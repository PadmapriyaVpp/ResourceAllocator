'''
Created on Aug 8, 2020

@author: Padmapriya
'''

class ResourceParam():
    def __init__(self):
        self.cpus: int = None
        self.price: float = None
        self.hours: int = None


class ResourceAllocator:

    def __init__(self):
        self.cputype_num = {
            "large": 1,
            "xlarge": 2,
            "2xlarge": 4,
            "4xlarge": 8,
            "8xlarge": 16,
            "10xlarge": 32
        }
        self.cpunum_type = {
            1: "large",
            2: "xlarge",
            4: "2xlarge",
            8: "4xlarge",
            16: "8xlarge",
            32: "10xlarge"
        }
        self.available_resource = {
            "us-east": {
                "large": 0.12,
                "xlarge": 0.23,
                "2xlarge": 0.45,
                "4xlarge": 0.774,
                "8xlarge": 1.4,
                "10xlarge": 2.82
            },
            "us-west": {
                "large": 0.14,
                "2xlarge": 0.413,
                "4xlarge": 0.89,
                "8xlarge": 1.3,
                "10xlarge": 2.97

            },
            "asia": {
                "large": 0.11,
                "2xlarge": 0.20,
                "4xlarge": 0.67,
                "8xlarge": 1.18,
            }
        }

    # *args - variable argument, **kwargs - key, value variable arguments
    def get_costs(self, **kwargs):
        resource_param = ResourceParam()
        list_server_details = []
        for k, v in kwargs.items():
            if k == 'cpus':
                resource_param.cpus = v
            if k == 'price':
                resource_param.price = v
            if k == 'hours':
                resource_param.hours = v

        if resource_param.cpus and resource_param.hours and resource_param.price is None:
            for region, cputype_costs in self.available_resource.items():
                list_cpus = cputype_costs.keys()
                dict_cputype_qty = self.get_cpus(
                    list_cpus, resource_param.cpus)  # servers
                total_cost = 0.0
                for cputype, qty in dict_cputype_qty.items():
                    total_cost = round(
                        total_cost + cputype_costs.get(cputype) * qty * resource_param.hours, 2)
                dict_server_details = {}
                dict_server_details["region"] = region
                dict_server_details["cpus"] = resource_param.cpus
                dict_server_details["hours"] = resource_param.hours
                dict_server_details["total_cost($)"] = total_cost
                dict_server_details["servers"] = dict_cputype_qty
                list_server_details.append(dict_server_details)
                
#         if resource_param.price and resource_param.hours and resource_param.cpus is None:
#             for region, cputype_costs in self.available_resource.items():
#                 list_cpus = cputype_costs.keys()
#                 dict_cputype_qty = self.get_cpus(
#                     list_cpus, resource_param.cpus)  # servers
#                 total_cost = 0.0
#                 for cputype, qty in dict_cputype_qty.items():
#                     total_cost = round(
#                         total_cost + cputype_costs.get(cputype) * qty * resource_param.hours, 2)
#                 dict_server_details = {}
#                 dict_server_details["region"] = region
#                 dict_server_details["cpus"] = resource_param.cpus
#                 dict_server_details["hours"] = resource_param.hours
#                 dict_server_details["total_cost($)"] = total_cost
#                 dict_server_details["servers"] = dict_cputype_qty
#                 list_server_details.append(dict_server_details)

        elif resource_param.price and resource_param.hours and resource_param.cpus is None:
            return None
        if resource_param.hours is None:
            return {"Error": "You must provide required hours."}
        if resource_param.cpus is None and resource_param.price is None:
            return {"Error": "You must provide required cpus or price."}

        return sorted(list_server_details, key=lambda k: k['total_cost($)'])

    def get_cpus(self, list_cpus, total_cpu):

        list_num_cpus_tcpu = self.get_list_cpus(total_cpu)
        dict_cputype_qty = {}
        list_num_cpus = []
        for cpu_type in list_cpus:
            num_cpus_fromtype = self.cputype_num.get(cpu_type)
            list_num_cpus.append(num_cpus_fromtype)
            for num_cpus in list_num_cpus_tcpu:
                if num_cpus == num_cpus_fromtype:
                    dict_cputype_qty[cpu_type] = 1

        list_num_cpus.sort(reverse=True)

        if len(list_num_cpus_tcpu) != len(dict_cputype_qty.values()):
            for num_cpus in list_num_cpus_tcpu:
                if num_cpus not in list_num_cpus:
                    for n_cpus in list_num_cpus:
                        if num_cpus % n_cpus == 0:
                            if dict_cputype_qty.get(self.cpunum_type.get(
                                        n_cpus)):
                                dict_cputype_qty[self.cpunum_type.get(
                                    n_cpus)] = dict_cputype_qty[self.cpunum_type.get(
                                        n_cpus)] + int(num_cpus / n_cpus)
                            else:
                                dict_cputype_qty[self.cpunum_type.get(
                                    n_cpus)] = int(num_cpus / n_cpus)
                            break
        return dict_cputype_qty
# [1, 2, 16, 32, 64]
# [1, 2, 16, 32]
# [1, 16, 64]

    def get_list_cpus(self, total_cpu):

        v = []
        list_cpus = []
        # Converting the decimal number
        # into its binary equivalent.
        while (total_cpu > 0):
            v.append(int(total_cpu % 2))
            total_cpu = int(total_cpu / 2)

        # Displaying the output when
        # the bit is '1' in binary
        # equivalent of number.
        for i in range(0, len(v)):
            if (v[i] == 1):
                list_cpus.append(pow(2, i))
        return list_cpus


if __name__ == "__main__":

    resource_allocator = ResourceAllocator()
    
    #case 1
    
    print(resource_allocator.get_costs(cpus=115, hours=24))
    print(resource_allocator.get_costs(cpus=145, hours=8))
    print(resource_allocator.get_costs(cpus=200, hours=10))
    print(resource_allocator.get_costs(cpus=1199, hours=10))
    #case 2
#     resource_allocator.get_costs(price=29, hours=8)
#     #case 3
#     resource_allocator.get_costs(cpus=214, price=95, hours=7)
#     resource_allocator.cpu_cost()
#     print(resource_allocator.get_list_cpus(115))
#     print(resource_allocator.get_cpus([1, 2, 4, 8, 16, 64], 115))
#     print(resource_allocator.get_cpus([2, 4, 8, 64], 29))
