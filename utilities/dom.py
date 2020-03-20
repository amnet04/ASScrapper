import csv
from asscrapper import logger

class dom():

    def __init__(self, strc_file, data_fields=[]):

        self.filename = strc_file
        self.strc_fields = ["LiCont", "ElCont", "Next", "End", "Captcha"]
        self.data_fields = data_fields
        self.main_strc = {}
        self.data_strc = {}
        self.check_strc()

    def check_strc(self):
        try:
            with open(self.filename, "r") as csvfile:
                data_strc = csv.DictReader(csvfile, delimiter="\t")
                if data_strc.fieldnames == ["Data", "Dom"]:
                    data_strc = [dict(x) for x in list(data_strc)]
                    
                    # Check containers and navigation fields
                    if [x["Data"] for x in data_strc[0:5]] == self.strc_fields: 
                        for data in data_strc[0:5]:
                            self.main_strc[data["Data"]] = {"Selector":data["Dom"]}
                    else:
                        raise ValueError("The first 5 rows must be: 'LiCont', 'ElCont', 'Next',  'End' and 'Captcha'")

                    # Check data fields
                    if self.data_fields != []:

                        if [x["Data"] for x in data_strc[5:]] == self.data_fields:
                            for data in data_strc[5:]:
                                self.data_strc[data["Data"]] = {"Selector":data["Dom"]}
                        else:
                            raise ValueError("The data rows must be: {}".format(self.data_fields))

                    else:
                        for data in data_strc[5:]:
                                self.data_strc[data["Data"]] = {"Selector":data["Dom"]}
                    
                else:
                    raise ValueError("CSV file header doesnt match, fields must be 'Data' and 'Dom' !!!!")

        except IOError as e:
            raise(e)


