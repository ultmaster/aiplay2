#include <bits/stdc++.h>

using namespace std;
#define fi first
#define se second
const int N = 25;

int values[N][N];
int sidec[2] = {1, -1};
FILE *reader[2], *writer[2];

void init() {
    for (int i = 0; i < 20; i++) {
        for (int j = 0; j < 20; j++) {
            values[i][j] = 0;
        }
    }
}

int count_score(int chess, const string& list_str) {
    int score = 0;
    if (list_str == "10000" || list_str == "01000" || list_str == "00100" || list_str == "00010" ||
        list_str == "00001") {
        score = 1;
    } else if (list_str == "11000") {
        score = 10;
    } else if (list_str == "10100") {
        score = 9;
    } else if (list_str == "10010") {
        score = 8;
    } else if (list_str == "10001") {
        score = 7;
    } else if (list_str == "01100") {
        score = 10;
    } else if (list_str == "01010") {
        score = 9;
    } else if (list_str == "01001") {
        score = 9;
    } else if (list_str == "00110") {
        score = 10;
    } else if (list_str == "00101") {
        score = 9;
    } else if (list_str == "00011") {
        score = 10;
    } else if (list_str == "11100") {
        score = 100;
    } else if (list_str == "11010") {
        score = 90;
    } else if (list_str == "11001") {
        score = 80;
    } else if (list_str == "10110") {
        score = 90;
    } else if (list_str == "10101") {
        score = 75;
    } else if (list_str == "10011") {
        score = 80;
    } else if (list_str == "01110") {
        score = 105;
    } else if (list_str == "01101") {
        score = 90;
    } else if (list_str == "01011") {
        score = 90;
    } else if (list_str == "11001") {
        score = 80;
    } else if (list_str == "11110") {
        score = 3000;
    } else if (list_str == "11101") {
        score = 2000;
    } else if (list_str == "11011") {
        score = 2000;
    } else if (list_str == "10111") {
        score = 2000;
    } else if (list_str == "01111") {
        score = 3000;
    } else if (list_str == "11111") {
        if (chess == 1) {
            score = 100000;
        } else if (chess == -1) {
            score = 50000;
        }
    }
    return score;
}

deque<int> get_list_left_right(int chess, int x, int y) {
    deque<int> list = {chess};
    for (int step = 1; step < 5; step++) {
        if (values[x][y - step] == chess * -1 || y - step < 0) {
            break;
        }
        list.push_front(values[x][y - step]);
    }
    for (int step = 1; step < 5; step++) {
        if (values[x][y + step] == chess * -1 || y + step >= 20) {
            break;
        }
        list.push_back(values[x][y + step]);
    }
    return list;
}

deque<int> get_list_up_down(int chess, int x, int y) {
    deque<int> list = {chess};
    for (int step = 1; step < 5; step++) {
        if (values[x - step][y] == chess * -1 || x - step < 0) {
            break;
        }
        list.push_front(values[x - step][y]);
    }
    for (int step = 1; step < 5; step++) {
        if (values[x + step][y] == chess * -1 || x + step >= 20) {
            break;
        }
        list.push_back(values[x + step][y]);
    }
    return list;
}

deque<int> get_list_down_ward(int chess, int x, int y) {
    deque<int> list = {chess};
    for (int step = 1; step < 5; step++) {
        if (values[x - step][y - step] == chess * -1 || x - step < 0 || y - step < 0) {
            break;
        }
        list.push_front(values[x - step][y - step]);
    }
    for (int step = 1; step < 5; step++) {
        if (values[x + step][y + step] == chess * -1 || x + step >= 20 || y + step > 20) {
            break;
        }
        list.push_back(values[x + step][y + step]);
    }
    return list;
}

deque<int> get_list_up_ward(int chess, int x, int y) {
    deque<int> list = {chess};
    for (int step = 1; step < 5; step++) {
        if (values[x - step][y + step] == chess * -1 || x - step < 0 || y + step >= 20) {
            break;
        }
        list.push_front(values[x - step][y + step]);
    }
    for (int step = 1; step < 5; step++) {
        if (values[x + step][y - step] == chess * -1 || x + step >= 20 || y - step < 0) {
            break;
        }
        list.push_back(values[x + step][y - step]);
    }
    return list;
}

deque<int> sub_vector(const deque<int>& d, const int pos, const int length) {
    return deque<int>(d.begin() + pos, d.begin() + pos + length);
}

string string_from_number(const int number) {
    stringstream sstr;
    sstr << number;
    string ret; sstr >> ret;
    return ret;
}

int get_total_score(int chess, deque<int> list) {
    int total_score = 0;
    static int turn = -1;
    turn++;
    if (list.size() < 5) {
        return 0;
    }
    for (int start = 0; start < list.size() - 4; start++) {
        deque<int> sub_list = sub_vector(list, start, 5);
        string sub_list_str = "";
        deque<int>::iterator iter;
        for (iter = sub_list.begin(); iter != sub_list.end(); ++iter) {
            if (*iter == -1) {
                *iter = 1;
            }
            sub_list_str += string_from_number(*iter);
        }
        int score = count_score(chess, sub_list_str);
        total_score += score;
    }
    return total_score;
}

pair<int, int> think() {
    int best_x = 0;
    int best_y = 0;
    int best_score = 0;
    //  遍历每一步棋
    for (int x = 0; x < 20; x++) {
        for (int y = 0; y < 20; y++) {
            if (values[x][y] != 0)
                continue;
            deque<int> left_right_red = get_list_left_right(1, x, y);
            deque<int> left_right_black = get_list_left_right(-1, x, y);
            deque<int> up_down_red = get_list_up_down(1, x, y);
            deque<int> up_down_black = get_list_up_down(-1, x, y);
            deque<int> down_ward_red = get_list_down_ward(1, x, y);
            deque<int> down_ward_black = get_list_down_ward(-1, x, y);
            deque<int> up_ward_red = get_list_up_ward(1, x, y);
            deque<int> up_ward_black = get_list_up_ward(-1, x, y);
            // 计算两种棋的四条线的分数
            int score_0 = get_total_score(1, left_right_red);
            int score_1 = get_total_score(-1, left_right_black);
            int score_2 = get_total_score(1, up_down_red);
            int score_3 = get_total_score(-1, up_down_black);
            int score_4 = get_total_score(1, down_ward_red);
            int score_5 = get_total_score(-1, down_ward_black);
            int score_6 = get_total_score(1, up_ward_red);
            int score_7 = get_total_score(-1, up_ward_black);
            deque<int> scores = {score_0, score_1, score_2, score_3, score_4, score_5, score_6, score_7};
            deque<int>::iterator iter;
            for (iter = scores.begin(); iter != scores.end(); ++iter) {
                if (*iter > best_score) {
                    best_score = *iter;
                    best_x = x;
                    best_y = y;
                }
            }
        }
    }
    return {best_x, best_y};
}

int judge() {
    deque<int> list0 = {1, 1, 1, 1, 1};
    deque<int> list1 = {-1, -1, -1, -1, -1};
    for (int i = 0; i < 20; i++) {
        for (int j = 0; j < 20; j++) {
            if (values[i][j] == 0)
                continue;
            deque<int> list = {values[i][j]};
            if (j + 1 < 20 || j + 2 < 20 || j - 1 >= 0 || j - 2 >= 0) {
                list.push_front(values[i][j - 1]);
                list.push_front(values[i][j - 2]);
                list.push_back(values[i][j + 1]);
                list.push_back(values[i][j + 2]);
                if (list == list0) {
                    return 1;
                } else if (list == list1) {
                    return -1;
                }
            }
            list.clear();
            // 纵向检测是否有一方胜利
            list.push_back(values[i][j]);
            if (i - 2 >= 0 || i - 1 >= 0 || i + 1 < 20 || i + 2 < 20) {
                list.push_front(values[i - 2][j]);
                list.push_front(values[i - 1][j]);
                list.push_back(values[i + 1][j]);
                list.push_back(values[i + 2][j]);
                if (list == list0) {
                    return 1;
                } else if (list == list1) {
                    return -1;
                }
            }
            list.clear();
            // 左上右下检测是否有一方胜利
            list.push_back(values[i][j]);
            if (i - 2 >= 0 || i - 1 >= 0 || j - 2 >= 0 || j - 1 >= 0 || i + 1 < 20 || i + 2 < 20 || j + 1 < 20 ||
                j + 2 < 20) {
                list.push_front(values[i - 2][j - 2]);
                list.push_front(values[i - 1][j - 1]);
                list.push_back(values[i + 1][j + 1]);
                list.push_back(values[i + 2][j + 2]);
                if (list == list0) {
                    return 1;
                } else if (list == list1) {
                    return -1;
                }
            }
            list.clear();
            // 右上左下检测是否有一方胜利
            list.push_back(values[i][j]);
            if (i - 2 >= 0 || i - 1 >= 0 || j + 2 < 20 || j + 1 < 20 || i + 1 < 20 || i + 2 < 20 || j - 1 >= 0 ||
                j - 2 >= 0) {
                list.push_front(values[i - 2][j + 2]);
                list.push_front(values[i - 1][j + 1]);
                list.push_back(values[i + 1][j - 1]);
                list.push_back(values[i + 2][j - 2]);
                if (list == list0) {
                    return 1;
                } else if (list == list1) {
                    return -1;
                }
            }
        }
    }
    return 0;
}

int last_x, last_y;

pair<int, int> ask(int x, int end = 0) {
    // ask side x
    fprintf(writer[x], "1 %d %d\n", last_x, last_y);  // 1 means you can carry on
    fflush(writer[x]);
    int p, q;
    fscanf(reader[x], "%d%d", &p, &q);
    printf("Drop(%d, %d, %d)\n", x, p, q);
    fflush(stdout);
    last_x = p; last_y = q;
    return {p, q};
}

void end(int x) {
    fprintf(writer[x], "0 -1 -1\n");
    fflush(writer[x]);
}

void process(int x) {
    while (true) {
        int acceptable;
        int p, q;
        scanf("%d%d%d", &acceptable, &p, &q);
        if (!acceptable)
            break;
        if (p != -1 && q == -1)
            values[p][q] = -x;
        auto ret = think();
        values[ret.first][ret.second] = x;
        printf("%d %d\n", ret.first, ret.second);
        fflush(stdout);
    }
}

int main(int argc, char* argv[]) {

    init();

    reader[0] = fdopen(atoi(argv[1]), "r");
    writer[0] = fdopen(atoi(argv[2]), "w");
    reader[1] = fdopen(atoi(argv[3]), "r");
    writer[1] = fdopen(atoi(argv[4]), "w");

    last_x = last_y = -1;
    int max_iter = 1000;
    while (max_iter--) {
        auto t1 = ask(0);
        if (values[t1.first][t1.second]) {
            puts("0,1");
            fflush(stdout);
            break;
        }
        values[t1.first][t1.second] = 1;
        if (judge() == 1) {
            end(0); end(1);
            puts("1,0");
            fflush(stdout);
            break;
        }
        auto t2 = ask(1);
        if (values[t2.first][t2.second]) {
            puts("1,0");
            fflush(stdout);
            break;
        }
        values[t2.first][t2.second] = -1;
        if (judge() == -1) {
            end(0); end(1);
            puts("0,1");
            fflush(stdout);
            break;
        }
    }
    fclose(reader[0]); fclose(writer[0]);
    fclose(reader[1]); fclose(writer[1]);
    if (max_iter <= 0) {
        puts("0,0");
        fflush(stdout);
    }
    return 0;
}
