import random
from datetime import timedelta, datetime
import pymongo
from include.functions import Functions
from include.setting import Settings
import matplotlib.pyplot as plt
import numpy as np


class Master:
    client = ''
    db_name = ''
    auctionID = ''
    countRequest = 0
    countMachine = 0
    countService = 0
    empty_machine = []
    myFunction = Functions()

    def __init__(self):
        self.connect_db()

    def connect_db(self):
        self.client = pymongo.MongoClient(Settings.MongoClientConnectionString)
        db = self.client.test

    def existDb(self, dbName):
        dblist = self.client.list_database_names()
        if dbName in dblist:
            return True
        return False

    def createDbStruct(self):
        randomString = self.myFunction.get_random_string(4)
        self.db_name = "auction_" + randomString
        print("Database Name: " + self.db_name)
        newDB = self.client[self.db_name]

        newDB.create_collection('auction')
        newDB.create_collection('user')
        newDB.create_collection('machine')
        newDB.create_collection('service')
        newDB.create_collection('request')
        newDB.create_collection('resourceAllocationNew')
        newDB.create_collection('resourceAllocationOld')
        print("collection created")
        return self.db_name

    def drop_allDatabase(self):
        for x in self.client.list_database_names():
            if (x != 'admin' and x != 'config' and x != 'local'):
                self.client.drop_database(x)

    def report11(self, databases):

        round = 0
        master_alloc_count = []
        for db in databases:
            temp_alloc_count = []
            mydb = self.client[db]
            user = mydb["user"]
            myUserDoc = user.find({'type': 'seller'}, sort=[("rank", pymongo.DESCENDING)])
            resourceAllocationNew = mydb["resourceAllocationNew"]

            for userDoc in myUserDoc:
                # https://stackoverflow.com/questions/4415514/in-mongodbs-pymongo-how-do-i-do-a-count
                alloc_count = resourceAllocationNew.count_documents({"sellerUserID": userDoc['_id'], 'isComplete': 1})
                temp_alloc_count.append(alloc_count)

            master_alloc_count.append(temp_alloc_count)
            round = round + 1

        y2 = []
        x2 = []
        c = 1
        # https://sparkbyexamples.com/numpy/numpy-array-mean-function/
        arr = np.array(master_alloc_count)
        arr1 = np.mean(arr, axis=0)
        sum_com = 0
        for av in arr1:
            sum_com = sum_com + av
            y2.append(av)
            x2.append('s' + str(c))
            c = c + 1

        # plotting the points
        plt.plot(x2, y2, color='green', linestyle='dashed', linewidth=2,
                 marker='o', markerfacecolor='blue', markersize=7)
        plt.title('Report 1-1(Resousrce Allocation is complete(new Algo))-sum: ' + str(sum_com))
        plt.show()

    def report12(self, databases):

        round = 0
        master_rank = []
        for db in databases:
            temp_rank = []
            mydb = self.client[db]
            user = mydb["user"]
            myUserDoc = user.find({'type': 'seller'}, sort=[("rank", pymongo.DESCENDING)])
            for userDoc in myUserDoc:
                temp_rank.append(userDoc['rank'])

            master_rank.append(temp_rank)
            round = round + 1

        y2 = []
        x2 = []
        c = 1
        # https://sparkbyexamples.com/numpy/numpy-array-mean-function/
        arr = np.array(master_rank)
        arr1 = np.mean(arr, axis=0)
        for av in arr1:
            y2.append(av)
            x2.append('s' + str(c))
            c = c + 1

        # plotting the points
        plt.plot(x2, y2, color='green', linestyle='dashed', linewidth=2,
                 marker='o', markerfacecolor='blue', markersize=7)
        plt.title('Report 1 - 2 (Rank Of Seller)')
        plt.show()

    def report13(self, databases):

        round = 0
        master_wallet = []
        for db in databases:
            temp_wallet = []
            mydb = self.client[db]
            user = mydb["user"]
            myUserDoc = user.find({'type': 'seller'}, sort=[("rank", pymongo.DESCENDING)])
            for userDoc in myUserDoc:
                temp_wallet.append(userDoc['walletWithNewAlgo'])

            master_wallet.append(temp_wallet)
            round = round + 1

        y2 = []
        x2 = []
        c = 1
        # https://sparkbyexamples.com/numpy/numpy-array-mean-function/
        arr = np.array(master_wallet)
        arr1 = np.mean(arr, axis=0)
        sum_of_wallet = 0
        for av in arr1:
            sum_of_wallet = sum_of_wallet + av
            y2.append(av)
            x2.append('s' + str(c))
            c = c + 1

        # plotting the points
        plt.plot(x2, y2, color='green', linestyle='dashed', linewidth=2,
                 marker='o', markerfacecolor='blue', markersize=7)
        plt.title('Report 1 - 3 (walletWithNewAlgo Of Seller) - Sum: ' + str(sum_of_wallet))
        plt.show()

    def report14(self, databases):

        round = 0
        master_wallet = []
        for db in databases:
            temp_wallet = []
            mydb = self.client[db]
            user = mydb["user"]
            myUserDoc = user.find({'type': 'seller'}, sort=[("rank", pymongo.DESCENDING)])

            for userDoc in myUserDoc:
                temp_wallet.append(userDoc['walletWithOldAlgo'])

            master_wallet.append(temp_wallet)
            round = round + 1

        y2 = []
        x2 = []
        c = 1
        # https://sparkbyexamples.com/numpy/numpy-array-mean-function/
        arr = np.array(master_wallet)
        arr1 = np.mean(arr, axis=0)
        sum_of_wallet = 0
        for av in arr1:
            sum_of_wallet = sum_of_wallet + av
            y2.append(av)
            x2.append('s' + str(c))
            c = c + 1

        # plotting the points
        plt.plot(x2, y2, color='green', linestyle='dashed', linewidth=2,
                 marker='o', markerfacecolor='blue', markersize=7)
        plt.title('Report 1 - 4 (walletWithOldAlgo Of Seller) - Sum: ' + str(sum_of_wallet))
        plt.show()

    def report15(self, databases):

        round = 0
        master_alloc_count = []
        for db in databases:
            temp_alloc_count = []
            mydb = self.client[db]
            user = mydb["user"]
            myUserDoc = user.find({'type': 'seller'}, sort=[("rank", pymongo.DESCENDING)])
            resourceAllocationOld = mydb["resourceAllocationOld"]

            for userDoc in myUserDoc:
                # https://stackoverflow.com/questions/4415514/in-mongodbs-pymongo-how-do-i-do-a-count
                alloc_count = resourceAllocationOld.count_documents({"sellerUserID": userDoc['_id'], 'isComplete': 1})
                temp_alloc_count.append(alloc_count)

            master_alloc_count.append(temp_alloc_count)
            round = round + 1

        y2 = []
        x2 = []
        c = 1
        # https://sparkbyexamples.com/numpy/numpy-array-mean-function/
        arr = np.array(master_alloc_count)
        arr1 = np.mean(arr, axis=0)
        sum_com = 0
        for av in arr1:
            sum_com = sum_com + av
            y2.append(av)
            x2.append('s' + str(c))
            c = c + 1

        # plotting the points
        plt.plot(x2, y2, color='green', linestyle='dashed', linewidth=2,
                 marker='o', markerfacecolor='blue', markersize=7)
        plt.title('Report1-5(Resousrce Allocation is complete(Old Algo))-Sum: ' + str(sum_com))
        plt.show()

    def report21(self, databases):

        round = 0
        master_alloc_count = []
        for db in databases:
            temp_alloc_count = []
            mydb = self.client[db]
            user = mydb["user"]
            myUserDoc = user.find({'type': 'seller'}, sort=[("rank", pymongo.DESCENDING)])
            resourceAllocationNew = mydb["resourceAllocationNew"]

            for userDoc in myUserDoc:
                # https://stackoverflow.com/questions/4415514/in-mongodbs-pymongo-how-do-i-do-a-count
                alloc_count = resourceAllocationNew.count_documents({"sellerUserID": userDoc['_id']})
                temp_alloc_count.append(alloc_count)

            master_alloc_count.append(temp_alloc_count)
            round = round + 1

        y2 = []
        x2 = []
        c = 1
        # https://sparkbyexamples.com/numpy/numpy-array-mean-function/
        arr = np.array(master_alloc_count)
        arr1 = np.mean(arr, axis=0)
        sum_com = 0
        for av in arr1:
            sum_com = sum_com + av
            y2.append(av)
            x2.append('s' + str(c))
            c = c + 1

        # plotting the points
        plt.plot(x2, y2, color='green', linestyle='dashed', linewidth=2,
                 marker='o', markerfacecolor='blue', markersize=7)
        plt.title('Report 2-1(Resousrce Allocation(New Algo + temp rank))-Sum: ' + str(sum_com))
        plt.show()

    def report31(self, databases):
        master_alloc_count = []
        for db in databases:
            mydb = self.client[db]
            resourceAllocationNew = mydb["resourceAllocationNew"]
            alloc_count = resourceAllocationNew.count_documents(
                {'isComplete': 1, 'DoneBycloudlet': 1})
            master_alloc_count.append(alloc_count)

        # https://sparkbyexamples.com/numpy/numpy-array-mean-function/
        arr = np.array(master_alloc_count)
        arr1 = np.mean(arr)
        print("Average Resousrce Allocation isComplete and DoneByCloudlet(new Algo): " + str(arr1))

    def report32(self, databases):

        master_alloc_count = []
        for db in databases:
            mydb = self.client[db]
            resourceAllocationNew = mydb["resourceAllocationNew"]
            alloc_count = resourceAllocationNew.count_documents(
                {'isComplete': 0})
            master_alloc_count.append(alloc_count)

        # https://sparkbyexamples.com/numpy/numpy-array-mean-function/
        arr = np.array(master_alloc_count)
        arr1 = np.mean(arr)
        print("Average Resousrce Allocation notComplete(new Algo): " + str(arr1))

    def report41(self, databases):

        round = 0
        master_alloc_count = []
        for db in databases:
            temp_alloc_count = []
            mydb = self.client[db]
            user = mydb["user"]
            myUserDoc = user.find({'type': 'buyer'}, sort=[("rank", pymongo.DESCENDING)])
            resourceAllocationNew = mydb["resourceAllocationNew"]

            for userDoc in myUserDoc:
                alloc_count = resourceAllocationNew.count_documents({"buyerUserID": userDoc['_id']})
                temp_alloc_count.append(alloc_count)

            master_alloc_count.append(temp_alloc_count)
            round = round + 1

        y2 = []
        x2 = []
        c = 1
        arr = np.array(master_alloc_count)
        arr1 = np.mean(arr, axis=0)
        sum_com = 0
        for av in arr1:
            sum_com = sum_com + av
            y2.append(av)
            x2.append('s' + str(c))
            c = c + 1

        # plotting the points
        plt.plot(x2, y2, color='green', linestyle='dashed', linewidth=2,
                 marker='o', markerfacecolor='blue', markersize=7)
        plt.title('Report 4-1(Buyer Winner sort By rank(New Algo))-Sum: ' + str(sum_com))
        plt.show()

    def report42(self, databases):

        round = 0
        master_alloc_count = []
        for db in databases:
            temp_alloc_count = []
            mydb = self.client[db]
            user = mydb["user"]
            myUserDoc = user.find({'type': 'buyer'}, sort=[("rank", pymongo.DESCENDING)])
            resourceAllocationOld = mydb["resourceAllocationOld"]

            for userDoc in myUserDoc:
                alloc_count = resourceAllocationOld.count_documents({"buyerUserID": userDoc['_id']})
                temp_alloc_count.append(alloc_count)

            master_alloc_count.append(temp_alloc_count)
            round = round + 1

        y2 = []
        x2 = []
        c = 1
        # https://sparkbyexamples.com/numpy/numpy-array-mean-function/
        arr = np.array(master_alloc_count)
        arr1 = np.mean(arr, axis=0)
        sum_com = 0
        for av in arr1:
            sum_com = sum_com + av
            y2.append(av)
            x2.append('s' + str(c))
            c = c + 1

        # plotting the points
        plt.plot(x2, y2, color='green', linestyle='dashed', linewidth=2,
                 marker='o', markerfacecolor='blue', markersize=7)
        plt.title('Report 4-1(Buyer Winner sort By rank(Old Algo))-Sum: ' + str(sum_com))
        plt.show()

    def report51(self, databases):
        master_alloc_difftime = []
        for db in databases:
            mydb = self.client[db]
            resourceAllocationOld = mydb["resourceAllocationOld"]
            resourceAllocationOldDoc = resourceAllocationOld.find()

            for allocDoc in resourceAllocationOldDoc:
                alloc_difftime = allocDoc['DiffTime']
                master_alloc_difftime.append(alloc_difftime)

        arr = np.array(master_alloc_difftime)
        arr1 = np.mean(arr)
        print("Diff Time Allocation(Old Algo): " + str(arr1))

    def report52(self, databases):
        master_alloc_difftime = []
        for db in databases:
            mydb = self.client[db]
            resourceAllocationNew = mydb["resourceAllocationNew"]
            resourceAllocationNewDoc = resourceAllocationNew.find()

            for allocDoc in resourceAllocationNewDoc:
                alloc_difftime = allocDoc['DiffTime']
                master_alloc_difftime.append(alloc_difftime)

        arr = np.array(master_alloc_difftime)
        arr1 = np.mean(arr)
        print("Diff Time Allocation(New Algo): " + str(arr1))


    def generate_user_by_type(self, type, count):
        # type => 'buyer' or 'seller'
        # randomtype => 0 = disable or 1 = enable
        mydb = self.client[self.db_name]
        mycol = mydb["user"]

        first_names = (
            'John', 'Andy', 'Joe', 'Ali', 'Meysam', 'Fateme', 'Negar', 'Keyvan', 'Haniye', 'Mahsa', 'Afsane', 'Sahar',
            'Baran', 'Pegah', 'Sara', 'Soozan', 'Farshad', 'Toofan', 'Erfan', 'Sepide', 'Shila', 'Niloofar', 'Aria',
            'Akbar', 'Farhad', 'Ghasem', 'Soraya', 'David', 'Ronaldo', 'Sina', 'Nima', 'Peter', 'Asghar', 'Nozhan',
            'Negin',
            'Ahmad', 'Kazem')

        for i in range(count):
            full_name = random.choice(first_names) + "_" + self.myFunction.get_random_string(4)
            mydict = {"name": full_name, "type": type, "rank": 0, "tempRank": 0, "walletWithNewAlgo": 0,
                      "walletWithOldAlgo": 0, "countOfRequest": 0}
            x = mycol.insert_one(mydict)

    def insertAuction(self, number):
        mydb = self.client[self.db_name]
        # now = datetime.now()
        mycol = mydb["auction"]

        mydict = {"ID": number, "startTimeNewAlgo": '', 'startTimeOldAlgo': '', "status": 'running'}

        x = mycol.insert_one(mydict)
        self.auctionID = number
        return {'auctionID': number}

    def generateMacineForSeller(self):
        mydb = self.client[self.db_name]

        mycol = mydb["machine"]
        user = mydb["user"]
        myquery = {"type": "seller"}
        mydoc = user.find(myquery)

        b = 0
        for do in mydoc:
            w_speed_process_MIPS = round(random.uniform(Settings.min_speed_process_MIPS,
                                                        Settings.max_speed_process_MIPS), 0)

            k = ''
            if (Settings.nCloudlet == 0):
                k = 0
            else:
                if (Settings.nCloudlet > b):
                    k = 1
                else:
                    k = 0

            mydict = {"ID": b, "auctionID": self.auctionID, "userID": do['_id'],
                      "proccessSpeed": w_speed_process_MIPS,
                      'isWinnerNewAlgo': 0,
                      'isWinnerOldAlgo': 0,
                      'isCloudlet': k
                      }
            b = b + 1

            x = mycol.insert_one(mydict)

    def generateRequestForBuyer(self):
        mydb = self.client[self.db_name]

        mycol = mydb["request"]

        user = mydb["user"]
        myquery = {"type": "buyer"}
        mydoc = user.find(myquery)

        c = 0
        for do in mydoc:
            deadline = datetime.now() + timedelta(
                minutes=round(random.uniform(Settings.min_minute_deadline, Settings.max_minute_deadline), 0))

            amount_cpu_cycle_MIPS = round(
                random.uniform(Settings.minCompulutionRequired_MIPS, Settings.maxCompulutionRequired_MIPS), 0)

            cost_task = round(self.myFunction.calculate_cost_task(Settings.cost_per_cpu_cycle, amount_cpu_cycle_MIPS),
                              2)

            budge = round(
                random.uniform(cost_task, cost_task + Settings.budge_increament_of_cost), 2)

            preferredPrice = round(
                random.uniform(cost_task, budge), 2)

            mydict = {"ID": c, "auctionID": self.auctionID, "userID": do['_id'],
                      'deadline': deadline.timestamp(), 'costTask': cost_task,
                      'requirementProccess': amount_cpu_cycle_MIPS, 'budge': budge,
                      'preferredPrice': preferredPrice,
                      'isWinnerNewAlgo': 0,
                      'isWinnerOldAlgo': 0
                      }
            c = c + 1

            x = mycol.insert_one(mydict)

            myquery = {"_id": do['_id']}
            newvalues = {"$set": {"countOfRequest": do['countOfRequest'] + 1}}
            user.update_one(myquery, newvalues)

        return

    def generateServicesForMachine(self):
        mydb = self.client[self.db_name]

        request = mydb["request"]
        myqueryReq = {"auctionID": self.auctionID}
        mydocRe = request.find(myqueryReq)

        c = 0
        for ra in mydocRe:
            requestID = ra['ID']
            costTask = ra['costTask']
            budge = ra['budge']
            deadline = ra['deadline']
            preferredPrice = ra['preferredPrice']
            requirementProccess = ra['requirementProccess']
            c = self.generateService(requestID, costTask, budge, preferredPrice, deadline, requirementProccess, c)

    def generateService(self, requestID, costTask, budge, preferredPrice, deadline, requirementProccess, c):
        mydb = self.client[self.db_name]
        mycol = mydb["service"]

        machine = mydb["machine"]
        myqueryMa = {"auctionID": self.auctionID}
        mydocMa = machine.find(myqueryMa)

        for ma in mydocMa:

            min_bid = (costTask - (Settings.alpha_decrement_of_cost * costTask))
            max_bid = preferredPrice  # budge
            bid = round(random.uniform(min_bid, max_bid), 2)

            startTime = datetime.now() + timedelta(
                minutes=round(random.uniform(Settings.min_minute_startTime, Settings.max_minute_startTime), 0))
            startTime = startTime.timestamp()
            proccessSpeed = ma['proccessSpeed']
            ttransition = round(
                random.uniform(Settings.min_second_transitionTime, Settings.max_second_transitionTime),
                0)
            Tcom = (requirementProccess / proccessSpeed) + ttransition
            if ((Tcom + startTime) <= deadline):
                if (ma['isCloudlet'] != 1):
                    mydict = {"ID": c, "auctionID": self.auctionID, "machineID": ma['ID'], "requestID": requestID,
                              "startTime": startTime,
                              'finishTime': deadline, 'bid': bid,
                              'isCloudlet': ma['isCloudlet'], 'timeTransition': ttransition}

                    mycol.insert_one(mydict)
                    c = c + 1
                else:
                    s = round(random.uniform(0, 10), 0)
                    if (s != 1):
                        mydict = {"ID": c, "auctionID": self.auctionID, "machineID": ma['ID'], "requestID": requestID,
                                  "startTime": startTime,
                                  'finishTime': deadline, 'bid': bid,
                                  'isCloudlet': ma['isCloudlet'], 'timeTransition': ttransition}

                        mycol.insert_one(mydict)
                        c = c + 1

        return c

    def generateTempRankSeller(self):
        mydb = self.client[self.db_name]

        user = mydb["user"]
        myquery = {"type": "seller"}
        mydoc = user.find(myquery)

        for do in mydoc:
            tempRank = round(random.uniform(Settings.MinTempRank,
                                            Settings.MaxTempRank), 0)
            tempRankFinal = do['tempRank'] + tempRank
            if (tempRank + do['rank'] >= Settings.LimitMaxRank):
                tempRankFinal = Settings.LimitMaxRank

            myquery = {"_id": do['_id']}
            newvalues = {"$set": {"tempRank": tempRankFinal}}
            user.update_one(myquery, newvalues)

    def update_rank(self, user_id, rank, rankType):

        mydb = self.client[self.db_name]
        user = mydb["user"]

        myquery = {"_id": user_id}
        newvalues = {"$set": {rankType: rank}}
        user.update_one(myquery, newvalues)

    def update_wallet(self, user_id, money, name_column):

        mydb = self.client[self.db_name]
        user = mydb["user"]

        myquery = {"_id": user_id}
        newvalues = {"$set": {name_column: money}}
        user.update_one(myquery, newvalues)

    def done_status_auction(self, id):

        mydb = self.client[self.db_name]
        auction = mydb["auction"]

        myquery = {"ID": id}
        newvalues = {"$set": {'status': 'done'}}
        auction.update_one(myquery, newvalues)

    def update_startTime_auction(self, id, columnName):
        mydb = self.client[self.db_name]
        auction = mydb["auction"]

        now = datetime.now()
        myquery = {"ID": id}
        newvalues = {"$set": {columnName: now.timestamp()}}
        auction.update_one(myquery, newvalues)

    def get_rank_user(self, user_id):
        mydb = self.client[self.db_name]
        user = mydb["user"]
        myquery_user = {"_id": user_id}
        mydoc_user = user.find_one(myquery_user)

        return {
            'totalRank': mydoc_user['rank'] + mydoc_user['tempRank'],
            'rank': mydoc_user['rank'],
            'tempRank': mydoc_user['tempRank']
        }

    def get_wallet(self, user_id):
        mydb = self.client[self.db_name]
        user = mydb["user"]
        myquery_user = {"_id": user_id}
        mydoc_user = user.find_one(myquery_user)

        return {
            'walletWithNewAlgo': mydoc_user['walletWithNewAlgo'],
            'walletWithOldAlgo': mydoc_user['walletWithOldAlgo'],
        }

    def print_info_solution_new_algo(self, temp_gici, temp_bjkj, chart=1):
        y2 = []
        x2 = []
        z = 0

        for J in range(len(temp_bjkj)):
            y2.append(temp_gici[temp_bjkj[J][0]][1] - temp_bjkj[J][2])
            x2.append('R' + str(temp_bjkj[J][0]) + "," + "M" + str(temp_bjkj[J][1]))
            z = z + 1

        if (chart == 1):
            # plotting the points
            plt.plot(x2, y2, color='green', linestyle='dashed', linewidth=2,
                     marker='o', markerfacecolor='blue', markersize=7)
            # naming the x axis
            plt.xlabel('State Space')
            # naming the y axis
            plt.ylabel('Evaluation Fitness Function')
            # giving a title to my graph
            plt.title('Resource allocation with hill climbing algorithm')
            # function to show the plot
            plt.xticks(rotation=90)
            plt.show()

        maxValue = np.max(y2)
        print("Global optimal solution Cost: " + str(maxValue))
        print("Count Allocation: " + str(z))

        # print("Global optimal solution index: " + str(np.where(y2 == maxValue)))

    def calculateCostAllocatin(self):
        mydb = self.client[self.db_name]
        size_r = 0
        size_m = 0
        size_s = 0
        request = mydb["request"]
        myquery_request = {"auctionID": self.auctionID, 'isWinnerNewAlgo': 0}
        mydoc_request = request.find(myquery_request)

        Machines = mydb["machine"]
        myquery_machine = {"auctionID": self.auctionID, 'isWinnerNewAlgo': 0}
        mydoc_machine = Machines.find(myquery_machine)

        Services = mydb["service"]

        temp_gici = []
        for re in mydoc_request:
            gici = [re['ID'], re['budge'] * re['costTask']]
            temp_gici.append(gici)
            size_r = size_r + 1

        # print('gi * ci -> before normalizatin')
        # print(temp_gici)

        temp_bjkj = []
        for ma in mydoc_machine:
            user_id = ma['userID']
            userRank = self.get_rank_user(user_id)
            size_m = size_m + 1
            temp_bjkj = self.myFunction.calc_temp_bjkj(ma, userRank['totalRank'], temp_bjkj, Services, self.auctionID)

        # print('bj / kj -> before normalizatin')
        # print(temp_bjkj)

        temp_gici = sorted(temp_gici, key=lambda x: x[1], reverse=True)
        max_gici = temp_gici[0]
        min_gici = temp_gici[len(temp_gici) - 1]
        dif_max_min_gici = max_gici[1] - min_gici[1]
        for m in range(len(temp_gici)):
            ts1 = (temp_gici[m][1] - min_gici[1])
            if (ts1 != 0):
                temp_gici[m] = [temp_gici[m][0], (temp_gici[m][1] - min_gici[1]) / dif_max_min_gici]
            else:
                temp_gici[m] = [temp_gici[m][0], 0]

        temp_gici = sorted(temp_gici, key=lambda x: x[0], reverse=False)
        # print('gi * ci -> After normalizatin')
        # print(temp_gici)

        temp_bjkj = sorted(temp_bjkj, key=lambda x: x[2], reverse=True)
        max_bjkj = temp_bjkj[0]
        min_bjkj = temp_bjkj[len(temp_bjkj) - 1]
        dif_max_min_bjkj = max_bjkj[2] - min_bjkj[2]
        for n in range(len(temp_bjkj)):
            ts2 = temp_bjkj[n][2] - min_bjkj[2]
            if (ts2 != 0):
                temp_bjkj[n] = [temp_bjkj[n][0], temp_bjkj[n][1],
                                (temp_bjkj[n][2] - min_bjkj[2]) / dif_max_min_bjkj]
            else:
                temp_bjkj[n] = [temp_bjkj[n][0], temp_bjkj[n][1], 0]

        # print('bj / kj -> After normalizatin')
        # print(temp_bjkj)

        allocationCost = []
        for isd in range(size_r):
            temp_m = []
            for jsd in range(size_m):
                temp_m.append('')
            allocationCost.append(temp_m)
        # print(allocationCost)

        for J in range(len(temp_bjkj)):
            allocationCost[temp_bjkj[J][0]][temp_bjkj[J][1]] = temp_gici[temp_bjkj[J][0]][1] - temp_bjkj[J][2]

        print(allocationCost)

        self.countRequest = size_r
        self.countMachine = size_m
        self.countService = size_s

        empty_machine = []
        for jsd in range(self.countMachine):
            empty_machine.append('')
        self.empty_machine = empty_machine
        return {
            'allocationCost': allocationCost,
            'temp_gici': temp_gici,
            'temp_bjkj': temp_bjkj
        }

    def randomSolution(self, ca):
        try:
            nR = random.randint(0, len(ca) - 1)
            nS = random.randint(0, len(ca[nR]) - 1)
            solution = [nR, nS]
        except:
            solution = [0, 0]

        # print("random solution:" + str(solution))
        return solution

    def calculateCost(self, ca, solution):
        try:
            cost = ca[solution[0]][solution[1]]
        except:
            cost = ''
        return cost

    def getNeighbours(self, ca, solution, mode):
        neighbours = []

        if (mode == 1):
            # neighbour by change service number
            nS = len(ca[solution[0]])
            for i in range(nS):
                neighbour = solution.copy()
                neighbour[0] = solution[0]
                if (i != solution[1]):
                    neighbour[1] = i
                    neighbourCost = self.calculateCost(ca, neighbour)
                    if (neighbourCost != ''):
                        neighbours.append(neighbour)
        elif (mode == 2):
            # neighbour by change Request number
            nR = len(ca)
            for i in range(nR):
                neighbour = solution.copy()
                neighbour[1] = solution[1]
                if (i != solution[0]):
                    neighbour[0] = i
                    neighbourCost = self.calculateCost(ca, neighbour)
                    if (neighbourCost != ''):
                        neighbours.append(neighbour)
                    # else:
                    #     if (ca[i] != []):
                    #         m = 0
                    #         while neighbourCost == '':
                    #             neighbour[1] = m
                    #             neighbourCost = self.calculateCost(ca, neighbour)
                    #             m = m + 1
                    #         neighbours.append(neighbour)

        # if (neighbours == []):
        #     if (mode == 1):
        #         mode = 2
        #     else:
        #         mode = 1
        #     neighbours = self.getNeighbours(ca, solution, mode)

        return neighbours

    def getBestNeighbour(self, ca, neighbours):
        # print("neighbours")
        # print(neighbours)
        # print("neighbours[0]")
        # print(neighbours[0])
        bestNeighbourCost = self.calculateCost(ca, neighbours[0])
        bestNeighbour = neighbours[0]
        for neighbour in neighbours:
            currentCost = self.calculateCost(ca, neighbour)
            if (currentCost != ''):
                if currentCost > bestNeighbourCost:
                    bestNeighbourCost = currentCost
                    bestNeighbour = neighbour
        return bestNeighbour, bestNeighbourCost

    def hillClimbing(self, ca):
        currentSolution = self.randomSolution(ca)
        currentCost = self.calculateCost(ca, currentSolution)
        # numberTry = 0
        # while currentCost == '':
        #     if (numberTry < Settings.numberTryRandomSolutionHillCimbing):
        #         currentSolution = self.randomSolution(ca)
        #         currentCost = self.calculateCost(ca, currentSolution)
        #         numberTry = numberTry + 1
        #     else:
        #         for sd in range(self.countRequest):
        #             for dl in range(self.countMachine):
        #                 if (ca[sd][dl] != ''):
        #                     currentSolution = [sd, dl]
        #                     currentCost = self.calculateCost(ca, currentSolution)
        #                     break
        if (currentCost == ''):
            for sd in range(self.countRequest):
                for dl in range(self.countMachine):
                    if (ca[sd][dl] != ''):
                        currentSolution = [sd, dl]
                        currentCost = self.calculateCost(ca, currentSolution)

        neighbours = self.getNeighbours(ca, currentSolution, 2)
        if (len(neighbours) != 0 and currentCost != ''):
            bestNeighbour, bestNeighbourCost = self.getBestNeighbour(ca, neighbours)
            while bestNeighbourCost > currentCost:
                currentSolution = bestNeighbour
                currentCost = bestNeighbourCost
                neighbours = self.getNeighbours(ca, currentSolution, 1)
                if (len(neighbours) != 0):
                    bestNeighbour, bestNeighbourCost = self.getBestNeighbour(ca, neighbours)

        return currentSolution, currentCost

    def update_database_after_alloc(self, result, DoneBycloudlet):
        mydb = self.client[self.db_name]
        mycol = mydb["resourceAllocationNew"]

        request = mydb["request"]
        Machines = mydb["machine"]
        service = mydb["service"]
        myquery_request = {"ID": result[0][0], "auctionID": self.auctionID}
        mydoc_request = request.find_one(myquery_request)

        myquery_machine = {"ID": result[0][1], "auctionID": self.auctionID}
        mydoc_machine = Machines.find_one(myquery_machine)

        myquery_service = {"machineID": result[0][1], "requestID": result[0][0], "auctionID": self.auctionID}
        mydoc_service = service.find_one(myquery_service)

        # update is_complete or not
        seller_rank = self.get_rank_user(mydoc_machine['userID'])
        if (mydoc_service['isCloudlet'] == 1):
            isComplete = 1
        else:
            isComplete = self.check_iscomplete_possibility(seller_rank["totalRank"])

        # insert on resource allocation table
        now = datetime.now()
        DiffTimeNewAlgo = mydoc_request['deadline'] - now.timestamp()
        mydict = {"auctionID": self.auctionID, "sellerUserID": mydoc_machine['userID'],
                  "buyerUserID": mydoc_request['userID'], 'isComplete': isComplete,
                  'finalPrice': mydoc_service['bid'], "DiffTime": DiffTimeNewAlgo, 'DoneBycloudlet': DoneBycloudlet}
        mycol.insert_one(mydict)

        # update iswinner machine and request for report
        newvalues = {"$set": {"isWinnerNewAlgo": 1}}
        Machines.update_one(myquery_machine, newvalues)
        request.update_one(myquery_request, newvalues)

        # update rank buyer
        if (DoneBycloudlet == 0):
            Buyer_rank = self.get_rank_user(mydoc_request['userID'])
            KCILevel = self.cal_KCILevel(mydoc_request['userID'])
            AverageNewRankBuyer = round((Buyer_rank["rank"] + KCILevel), 2)
            self.update_rank(mydoc_request['userID'], AverageNewRankBuyer, 'rank')

        # update rank seller
        if (isComplete == 0):
            self.update_rank(mydoc_machine['userID'], 0, 'tempRank')
            AverageNewRankSeller = round((seller_rank["rank"] + (Settings.kBDLevel)), 2)
            if (AverageNewRankSeller <= Settings.LimitMinRank):
                AverageNewRankSeller = Settings.LimitMinRank
            self.update_rank(mydoc_machine['userID'], AverageNewRankSeller, 'rank')
        else:
            KBILevel = self.calc_KBILevel(mydoc_request['requirementProccess'], mydoc_machine['proccessSpeed'],
                                          mydoc_service['startTime'], mydoc_request['deadline'], mydoc_request['budge'],
                                          mydoc_request['preferredPrice'], mydoc_service['bid'],
                                          mydoc_service['timeTransition'])

            AverageNewRankSeller = round((seller_rank["rank"] + (KBILevel)), 2)
            if (AverageNewRankSeller >= Settings.LimitMaxRank):
                AverageNewRankSeller = Settings.LimitMaxRank

            self.update_rank(mydoc_machine['userID'], AverageNewRankSeller, 'rank')
            # update wallet seller
            currenttWalletSeller = self.get_wallet(mydoc_machine['userID'])
            newWalletSeller = currenttWalletSeller['walletWithNewAlgo'] + mydoc_service['bid']
            self.update_wallet(mydoc_machine['userID'], newWalletSeller, "walletWithNewAlgo")

        return isComplete

    def calc_KBILevel(self, cc, w, ts, deadline, budge, preferredPrice, bid, ttransition):
        Tcom = (cc / w) + ttransition
        tmin = Tcom + ts
        tmax = deadline
        Rank1 = (deadline - ts) / (tmax - tmin)

        z = budge - preferredPrice
        h = budge - bid
        rank2 = 0
        if (bid > preferredPrice):
            rank2 = (z - h) / z
        else:
            rank2 = Settings.epsilon

        KBILevel = Rank1 / rank2
        return round(KBILevel * Settings.k_forkbilevel, 2)

    def cal_KCILevel(self, userID):
        mydb = self.client[self.db_name]
        user = mydb["user"]
        myquery_user = {"_id": userID}
        mydoc_user = user.find_one(myquery_user)
        services = mydoc_user['countOfRequest']

        maxm = mydb.user.find_one({}, sort=[("countOfRequest", pymongo.DESCENDING)])
        maxm = maxm["countOfRequest"]
        if (maxm == 0):
            maxm = 1

        utility = round(random.uniform(80, 90), 0) / 100
        kCILevel = ((services / maxm) / ((1 - utility) + Settings.epsilon)) * Settings.y_forkCILevel
        return round(kCILevel, 2)

    def check_iscomplete_possibility(self, rank):
        s = ''
        if (rank < 1):
            s = round(random.uniform(0, 10), 0)
        elif (1 <= rank < 10):
            s = round(random.uniform(0, 20), 0)
        elif (10 <= rank < 25):
            s = round(random.uniform(0, 25), 0)
        elif (25 <= rank < 50):
            s = round(random.uniform(0, 50), 0)
        elif (50 <= rank < 75):
            s = round(random.uniform(0, 75), 0)
        elif (75 <= rank < 100):
            s = round(random.uniform(0, 100), 0)
        elif (100 <= rank):
            s = round(random.uniform(0, 100), 0)

        if (s == 1):
            # not complete
            return 0
        else:
            # is complete
            return 1

    def check_iscomplete_possibility_old_algo(self):
        s = round(random.uniform(0, 10), 0)
        if (s == 1):
            # not complete
            return 0
        else:
            # is complete
            return 1

    def clean_costAlloc(self, ca, result):
        ca[result[0][0]] = self.empty_machine
        for isd in range(self.countRequest):
            ca[isd][result[0][1]] = ""
        return ca

    def get_process_speed_by_machineID(self, machineID):

        mydb = self.client[self.db_name]
        machine = mydb["machine"]
        myquery_machine = {"ID": machineID}
        mydoc_machine = machine.find_one(myquery_machine)

        return mydoc_machine['proccessSpeed']

    def alloc_to_cloudlet(self, result):
        mydb = self.client[self.db_name]
        service = mydb["service"]
        myquery_service = {"auctionID": self.auctionID, 'isCloudlet': 1, 'requestID': result[0][0]}
        mydoc_services = service.find(myquery_service)
        temp_wibi = []

        for se in mydoc_services:
            bjwj = [se['machineID'], self.get_process_speed_by_machineID(se['machineID']) / se['bid']]
            temp_wibi.append(bjwj)
            print(temp_wibi)
        if (len(temp_wibi) != 0):
            print(temp_wibi)
            temp_wibi = sorted(temp_wibi, key=lambda x: x[1], reverse=True)
            max_wibi = temp_wibi[0]
            result[0][1] = max_wibi[0]
            return result

        return ''

    def runMyAlgorithm(self, ca):
        print("*** New Algo ***")
        for i in range(self.countRequest):
            result = self.hillClimbing(ca)
            if (result[1] != ''):
                print(str(i) + " : " + str(result))
                self.clean_costAlloc(ca, result)
                isComplete = self.update_database_after_alloc(result, 0)

                # run algo2 if not complete
                if (isComplete == 0):
                    alloc = self.alloc_to_cloudlet(result)
                    if (alloc != ''):
                        self.update_database_after_alloc(alloc, 1)
                        print("update_database_after_alloc")

    def runOldAlgorithm(self):
        print("*** Old Algo ***")
        mydb = self.client[self.db_name]

        mycol = mydb["resourceAllocationOld"]

        request = mydb["request"]
        myquery_request = {"auctionID": self.auctionID, 'isWinnerOldAlgo': 0}
        mydoc_request = request.find(myquery_request)

        Machines = mydb["machine"]
        myquery_machine = {"auctionID": self.auctionID, 'isWinnerOldAlgo': 0}
        mydoc_machine = Machines.find(myquery_machine)

        Services = mydb["service"]

        temp_cidi = []
        for re in mydoc_request:
            cidi = [re['ID'], re['costTask'] / re['deadline']]
            temp_cidi.append(cidi)
        temp_cidi = sorted(temp_cidi, key=lambda x: x[1], reverse=True)

        temp_biwi = []
        for ma in mydoc_machine:
            myquery_Services = {"machineID": ma['ID'], "auctionID": self.auctionID}
            mydoc_Services = Services.find(myquery_Services)
            for se in mydoc_Services:
                bjwj = [se['requestID'], se['machineID'], se['ID'], se['bid'] / ma['proccessSpeed']]
                temp_biwi.append(bjwj)
        temp_biwi = sorted(temp_biwi, key=lambda x: x[3], reverse=False)

        for j in range(len(temp_cidi)):
            for h in range(len(temp_biwi)):
                request_isWinner_status = self.get_data_request_by_id(temp_cidi[j][0], 'isWinnerOldAlgo')
                machine_isWinner_status = self.get_data_machine_by_id(temp_biwi[h][1], 'isWinnerOldAlgo')
                if (machine_isWinner_status != 1 and request_isWinner_status != 1):
                    if (temp_biwi[h][0] == temp_cidi[j][0]):

                        dt_r = self.get_data_request_by_id(temp_cidi[j][0], 'deadline')
                        dt_s = self.get_data_service_by_id(temp_biwi[h][2], 'startTime')
                        requirementProccess = self.get_data_request_by_id(temp_cidi[j][0], 'requirementProccess')
                        proccessSpeed = self.get_data_machine_by_id(temp_biwi[h][1], 'proccessSpeed')
                        ttransition = self.get_data_service_by_id(temp_biwi[h][2], 'timeTransition')

                        Tcom = (requirementProccess / proccessSpeed) + ttransition

                        if ((Tcom + dt_s) <= dt_r):
                            print(str(j) + " : [" + str(temp_cidi[j][0]) + ", " + str(temp_biwi[h][1]) + "]")

                            now = datetime.now()
                            G_time = self.calc_G_time()
                            DiffTimeOldAlgo = dt_r - (now.timestamp() - G_time)

                            costTask = self.get_data_request_by_id(temp_cidi[j][0], 'costTask')
                            bid = self.get_data_service_by_id(temp_biwi[h][2], 'bid')

                            request_userID = self.get_data_request_by_id(temp_cidi[j][0], 'userID')
                            machine_userID = self.get_data_machine_by_id(temp_biwi[h][1], 'userID')
                            isComplete = self.check_iscomplete_possibility_old_algo()

                            # insert on resource allocation table
                            mydict = {"auctionID": self.auctionID, "sellerUserID": machine_userID,
                                      "buyerUserID": request_userID, 'isComplete': isComplete,
                                      'finalPrice': bid, "DiffTime": DiffTimeOldAlgo}
                            mycol.insert_one(mydict)

                            # update iswinner machine and request for report
                            newvalues = {"$set": {"isWinnerOldAlgo": 1}}
                            myquery2_machine = {"ID": temp_biwi[h][1], "auctionID": self.auctionID}
                            Machines.update_one(myquery2_machine, newvalues)
                            myquery2_request = {"ID": temp_cidi[j][0], "auctionID": self.auctionID}
                            request.update_one(myquery2_request, newvalues)

                            # update wallet seller
                            if (isComplete == 1):
                                currenttWalletSeller = self.get_wallet(machine_userID)
                                newWalletSeller = currenttWalletSeller['walletWithOldAlgo'] + bid
                                self.update_wallet(machine_userID, newWalletSeller, "walletWithOldAlgo")

    def calc_G_time(self):
        mydb = self.client[self.db_name]
        auction = mydb["auction"]
        myquery_auction = {"ID": self.auctionID}
        mydoc_auction = auction.find_one(myquery_auction)

        return (mydoc_auction['startTimeOLDAlgo'] - mydoc_auction['startTimeNewAlgo'])

    def get_data_request_by_id(self, requestID, dataname):
        mydb = self.client[self.db_name]
        request = mydb["request"]
        myquery_request = {"ID": requestID, "auctionID": self.auctionID}
        mydoc_request = request.find_one(myquery_request)

        return mydoc_request[dataname]

    def get_data_service_by_id(self, serviceID, dataname):
        mydb = self.client[self.db_name]
        service = mydb["service"]
        myquery_service = {"ID": serviceID, "auctionID": self.auctionID}
        mydoc_service = service.find_one(myquery_service)

        return mydoc_service[dataname]

    def get_data_machine_by_id(self, machineID, dataname):
        mydb = self.client[self.db_name]
        machine = mydb["machine"]
        myquery_machine = {"ID": machineID, "auctionID": self.auctionID}
        mydoc_machine = machine.find_one(myquery_machine)

        return mydoc_machine[dataname]
