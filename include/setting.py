# auction Settings
class Settings:
    # MongoClientConnectionString = "mongodb+srv://k1ahani:keyvan@cluster0.aou8mur.mongodb.net/?retryWrites=true&w=majority"
    MongoClientConnectionString = "mongodb://localhost:27017"

    nAuction = 30
    nBuyer = 10
    nSeller = 10
    nCloudlet = 0
    min_minute_deadline = 15
    max_minute_deadline = 60
    MinTempRank = 0
    MaxTempRank = 50

    budge_increament_of_cost = 5
    preferredPrice_increament_of_cost = 5
    minCompulutionRequired_MIPS = 5000000
    maxCompulutionRequired_MIPS = 10000000

    alpha_decrement_of_cost = 0.2
    cost_per_cpu_cycle = 0.000001
    min_speed_process_MIPS = 5000
    max_speed_process_MIPS = 10000
    min_minute_startTime = 5
    max_minute_startTime = 10
    y_forkCILevel = 0.05

    k_forkbilevel = 0.000000001
    epsilon = 0.000000001
    min_second_transitionTime = 30
    max_second_transitionTime = 70
    LimitMinRank = -10
    LimitMaxRank = 1000
    kBDLevel = -2
    # numberTryRandomSolutionHillCimbing = 1
