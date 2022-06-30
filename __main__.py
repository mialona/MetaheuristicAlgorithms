from data import load_data, create_data
from local_search import local_search_algorithm
from genetic import genetic_algorithm
from gm_eda import gm_eda

if __name__ == '__main__':
    # Test features
    features = {
        "Xmin": 0,
        "Xmax": 2500,
        "Ymax": 500,
        "M1_head_A": 2000,
        "M2_head_B": 500,
        "M3_collision": 500,

        # Extensions
        "exten_head_A": 0,
        "exten_head_B": 0
    }

    # Test data load/create
    data = load_data('data/data_example.xlsx')
    #data = create(features, 25, 25, True)

    # Test data show
    print("  ops       t       x       y   seq")
    for line in data:
        print("%5d " % (line[0]), end="")
        print("%7.2f " % (line[1]), end="")
        print("%7.2f " % (line[2]), end="")
        print("%7.2f " % (line[3]), end="")
        print("%5d " % (line[4]), end="")
        print("")
    print("\n")


    ##########################
    # Local Search algorithm #
    ##########################

    # Algorithm execution
    best_head_a, best_head_b, total_historical, best_historical = local_search_algorithm(features, data, 5, 500)
    print("Local Search:", best_historical[len(best_historical) - 1])

    # Operations to perform on the first head according to the best solution obtained
    print("\n  ops     t  t_start")
    for line in best_head_a:
        print("%5d " % (line[0]), end="")
        print("%7.2f " % (line[1]), end="")
        print("%7.2f " % (line[2]), end="")
        print('')

    # Operations to perform on the first head according to the best solution obtained
    print("\n  ops       t t_start")
    for line in best_head_b:
        print("%5d " % (line[0]), end="")
        print("%7.2f " % (line[1]), end="")
        print("%7.2f " % (line[2]), end="")
        print('')


    #####################
    # Genetic algorithm #
    #####################

    # Algorithm execution
    d_head_a, d_head_b, historical, ops_a, ops_b, percent = genetic_algorithm(features, data, 499, 0.15)
    print("\nGenetic algorithm:", percent)

    # Operations to perform on the first head according to the best solution obtained
    print("\n  ops     t  t_start")
    for line in d_head_a:
        print("%5d " % (line[0]), end="")
        print("%7.2f " % (line[1]), end="")
        print("%7.2f " % (line[2]), end="")
        print('')

    # Operations to perform on the first head according to the best solution obtained
    print("\n  ops       t t_start")
    for line in d_head_b:
        print("%5d " % (line[0]), end="")
        print("%7.2f " % (line[1]), end="")
        print("%7.2f " % (line[2]), end="")
        print('')


    ##########
    # GM-EDA #
    ##########

    # Algorithm execution
    d_head_a, d_head_b, historical, best_ops_a, best_ops_b, percent = gm_eda(features, data, 3, 10)
    print("\nGM-EDA:", percent)

    # Operations to perform on the first head according to the best solution obtained
    print("\n  ops     t  t_start")
    for line in d_head_a:
        print("%5d " % (line[0]), end="")
        print("%7.2f " % (line[1]), end="")
        print("%7.2f " % (line[2]), end="")
        print('')

    # Operations to perform on the first head according to the best solution obtained
    print("\n  ops       t t_start")
    for line in d_head_b:
        print("%5d " % (line[0]), end="")
        print("%7.2f " % (line[1]), end="")
        print("%7.2f " % (line[2]), end="")
        print('')