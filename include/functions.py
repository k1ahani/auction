import datetime
from datetime import datetime
import random
import string


class Functions:

    def calculate_cost_task(self, cost_per_cpu_cycle, compulutioan_required_cpu_cycle_MIPS):
        Cost = cost_per_cpu_cycle * compulutioan_required_cpu_cycle_MIPS

        return Cost

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def calc_temp_bjkj(self, ma, totalRank, temp_bjkj,Services,auctionID):

        myquery_Services = {"machineID": ma['ID'], "auctionID": auctionID}
        mydoc_Services = Services.find(myquery_Services)

        for se in mydoc_Services:
            if (totalRank == 0):
                bjkj = [se['requestID'], se['machineID'], 0]
            else:
                bjkj = [se['requestID'], se['machineID'], se['bid'] / totalRank]
            temp_bjkj.append(bjkj)

        return temp_bjkj

