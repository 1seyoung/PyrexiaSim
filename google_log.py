import pygsheets

class Google_update():
    def __init__(self):
        self.gc = pygsheets.authorize(service_file="gss.json")
        self.sh = self.gc.open("PurexiaSim__Data")
        self.wks = self.sh.worksheet('title','log')



    def update_log(self, text_):
        df = self.wks.get_as_df()            
        #self.wks.update_row((len(df)+2),text_,col_offset=0)
        self.wks.append_table(text_, start='A1', end=None, dimension='ROWS', overwrite=False)