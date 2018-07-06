# -*- coding: utf-8 -*-


def rank_generation(team_info, now_rank, match_info):
    all_match_result = [3, 1, 0]
    # team_info = raw_input("请输入小组中的队伍名称：")
    team_list = [team for team in team_info.split()]
    # now_rank = raw_input('请输入小组当前积分：')
    rank_list = [int(rank) for rank in now_rank.split()]
    # match_info = raw_input('请输入小组中的当前对决：')
    match_list = [match for match in match_info.split()]
    # print team_list, rank_list, match_list
    first_match = match_list[0]
    second_match = match_list[1]
    for first_match_result in all_match_result:
        for second_match_result in all_match_result:
            if first_match_result == 3:
                rank_list[int(first_match.split('v')[0]) - 1] += 3
            elif first_match_result == 1:
                rank_list[int(first_match.split('v')[0]) - 1] += 1
                rank_list[int(first_match.split('v')[1]) - 1] += 1
            elif first_match_result == 0:
                rank_list[int(first_match.split('v')[1]) - 1] += 3
            if second_match_result == 3:
                rank_list[int(second_match.split('v')[0]) - 1] += 3
            elif second_match_result == 1:
                rank_list[int(second_match.split('v')[0]) - 1] += 1
                rank_list[int(second_match.split('v')[1]) - 1] += 1
            elif second_match_result == 0:
                rank_list[int(second_match.split('v')[1]) - 1] += 3
            print first_match_result, second_match_result
            new_team_list = []
            new_rank_list = []
            out_num = []
            max_rank = 0
            team_num = 4
            while team_num:
                for i in range(4):
                    if i+1 in out_num:
                        continue
                    if max_rank in out_num:
                        max_rank += 1
                    if i < 4:
                        out_num.append(max_rank)
                        break
                    if rank_list[max_rank] < rank_list[i+1]:
                        max_rank = i+1
                new_team_list.append(team_list[max_rank])
                new_rank_list.append(rank_list[max_rank])
                team_num = team_num - 1
            for i in range(4):
                print new_team_list[i], new_rank_list[i]
            rank_list = [int(rank) for rank in now_rank.split()]




# 法国 丹麦 澳大利亚 秘鲁
# 3 3 0 0
# 1v4 2v3



if __name__ == "__main__":
    rank_generation('墨西哥 瑞典 韩国 德国', '3 3 0 0', '1v3 2v4')