import csv

class dom():

    def __init__(self, strc_file, data_fields=[]):

        print("\n********* ---> Configurando el dom <--- *********")
        self.filename = strc_file
        self.strc_fields = ["LiCont", "ElCont", "Next", "End", "Captcha"]
        self.data_fields = data_fields
        self.main_str = {}
        self.data_str = {}
        self.check_strc()
        print("********* ---> Dom configurado     <--- *********\n")


    def check_strc(self):
        print("********* ---> Chequeando estructura")
        try:
            with open(self.filename, "r") as csvfile:
                data_str = csv.DictReader(csvfile, delimiter="\t")
                if data_str.fieldnames == ["Data", "Dom"]:
                    data_str = [dict(x) for x in list(data_str)]
                    
                    # Check containers and navigation fields
                    if [x["Data"] for x in data_str[0:5]] == self.strc_fields: 
                        for data in data_str[0:5]:
                            self.main_str[data["Data"]] = data["Dom"]
                    else:
                        raise ValueError("The first 5 rows must be: 'LiCont', 'ElCont', 'Next',  'End' and 'Captcha'")

                    # Check 
                    if self.data_fields != []:

                        if [x["Data"] for x in data_str[5:]] == self.data_fields:
                            for data in data_str[5:]:
                                self.data_str[data["Data"]] = data["Dom"]
                        else:
                            raise ValueError("The data rows must be: {}".format(self.data_fields))

                    else:
                        for data in data_str[5:]:
                                self.data_str[data["Data"]] = data["Dom"]
                    
                else:
                    raise ValueError("csvfile header doesnt match, fields must be 'Data' and 'Dom' !!!!")

        except IOError as e:
            raise(e)
        print("********* ---> Estructura chequeada")

DOM = dom("/home/sarnahorn/Programacion/Doctorado/asscrapper/examples/free-proxy-list-dot_net.csv", 
          ["Ip","Port","Https","Country","Anonymity"])
print(DOM.main_str, "\n\n",DOM.data_str)
