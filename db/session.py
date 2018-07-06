# -*- coding: utf-8 -*-
"""
Created on 2017-7-12
@author: lsy
"""
import time

from sqlalchemy.exc import DisconnectionError, OperationalError

import sqlalchemy.orm
import sqlalchemy.event
import sqlalchemy.engine

from sqlalchemy.pool import NullPool, StaticPool


# import vsm.flags as flags
import logging
# from common.exception import DataBaseException as exception


LOG = logging.getLogger(__name__)

_ENGINE = None
_MAKER = None


def get_session(autocommit=True, expire_on_commit=False):
    """Return a SQLAlchemy session."""
    global _MAKER

    if _MAKER is None:
        engine = get_engine()
        _MAKER = get_maker(engine, autocommit, expire_on_commit)
    session = _MAKER()
    return session


def synchronous_switch_listener(dbapi_conn, connection_rec):
    """Switch sqlite connections to non-synchronous mode"""
    dbapi_conn.execute("PRAGMA synchronous = OFF")


def ping_listener(dbapi_conn, connection_rec, connection_proxy):
    """
    Ensures that MySQL connections checked out of the
    pool are alive.

    Borrowed from:
    http://groups.google.com/group/sqlalchemy/msg/a4ce563d802c929f
    """
    try:
        dbapi_conn.cursor().execute('select 1')
    except dbapi_conn.OperationalError, ex:
        if ex.args[0] in (2006, 2013, 2014, 2045, 2055):
            LOG.warn('Got mysql server has gone away: %s', ex)
            raise DisconnectionError("Database server went away")
        else:
            raise


def is_db_connection_error(args):
    """Return True if error in connecting to db."""
    # NOTE(adam_g): This is currently MySQL specific and needs to be extended
    #               to support Postgres and others.
    conn_err_codes = ('2002', '2003', '2006')
    for err_code in conn_err_codes:
        if args.find(err_code) != -1:
            return True
    return False


def get_engine():
    """Return a SQLAlchemy engine."""
    global _ENGINE
    sql_connection = 'mysql://root:123456@127.0.0.1:3306/jindou_system?charset=utf8'
    if _ENGINE is None:
        connection_dict = sqlalchemy.engine.url.make_url(sql_connection)

        engine_args = {
            "pool_recycle": 3600,
            "echo": False,
            'convert_unicode': True,
        }

        # Map our SQL debug level to SQLAlchemy's options
#         if FLAGS.sql_connection_debug >= 100:
#             engine_args['echo'] = 'debug'
#         elif FLAGS.sql_connection_debug >= 50:
#             engine_args['echo'] = True

        if "sqlite" in connection_dict.drivername:
            engine_args["poolclass"] = NullPool

            if sql_connection == "sqlite://":
                engine_args["poolclass"] = StaticPool
                engine_args["connect_args"] = {'check_same_thread': False}

        _ENGINE = sqlalchemy.create_engine(sql_connection, **engine_args)

        if 'mysql' in connection_dict.drivername:
            sqlalchemy.event.listen(_ENGINE, 'checkout', ping_listener)
        elif "sqlite" in connection_dict.drivername:
            sqlalchemy.event.listen(_ENGINE, 'connect',
                                        synchronous_switch_listener)

        try:
            _ENGINE.connect()
        except OperationalError, e:
            if not is_db_connection_error(e.args[0]):
                raise

            remaining = 10
            if remaining == -1:
                remaining = 'infinite'
            while True:
                msg = ('SQL connection failed. %s attempts left.')
                LOG.warn(msg % remaining)
                if remaining != 'infinite':
                    remaining -= 1
                time.sleep(10)
                try:
                    _ENGINE.connect()
                    break
                except OperationalError, e:
                    if ((remaining != 'infinite' and remaining == 0) or
                            not is_db_connection_error(e.args[0])):
                        raise
    return _ENGINE


def get_maker(engine, autocommit=True, expire_on_commit=False):
    """Return a SQLAlchemy sessionmaker using the given engine."""
    return sqlalchemy.orm.sessionmaker(bind=engine,
                                       autocommit=autocommit,
                                       expire_on_commit=expire_on_commit)


if __name__ == '__main__':
    engine = get_engine()
    session = get_session(engine)