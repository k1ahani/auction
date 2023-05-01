# -*- coding: utf-8 -*-
from __future__ import division
from include.setting import Settings
from include.master import Master
from include.functions import Functions

if __name__ == "__main__":
    myMaster = Master()
    myFunc = Functions()

    databases_name = []
    for s in range(100):
        dbName = myMaster.createDbStruct()
        databases_name.append(dbName)
        myMaster.generate_user_by_type('seller', Settings.nSeller)
        myMaster.generate_user_by_type('buyer', Settings.nBuyer)

        for i in range(Settings.nAuction):
            print("Run Auction:" + str(i + 1))
            resInsertAuction = myMaster.insertAuction(i)
            myMaster.generateMacineForSeller()
            myMaster.generateRequestForBuyer()
            myMaster.generateServicesForMachine()
            myMaster.generateTempRankSeller()
            myMaster.update_startTime_auction(i, 'startTimeNewAlgo')
            data = myMaster.calculateCostAllocatin()
            myMaster.runMyAlgorithm(data["allocationCost"])

            myMaster.update_startTime_auction(i, 'startTimeOLDAlgo')
            myMaster.runOldAlgorithm()

            myMaster.done_status_auction(i)
            # myMaster.print_info_solution_new_algo(data["temp_gici"], data["temp_bjkj"])
            i = i + 1

    # myMaster.report11(databases_name)
    # myMaster.report12(databases_name)
    # myMaster.report13(databases_name)
    # myMaster.report14(databases_name)
    # myMaster.report15(databases_name)
    # myMaster.report21(databases_name)
    # myMaster.report31(databases_name)
    # myMaster.report32(databases_name)
    #myMaster.report41(databases_name)
    #myMaster.report42(databases_name)
    myMaster.report51(databases_name)
    myMaster.report52(databases_name)
    myMaster.drop_allDatabase()
