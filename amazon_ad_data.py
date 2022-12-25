import csv
import pandas as pd
import numpy as np
import itertools as it
import tkinter as tk
import subprocess
import os

ad_file = "st_report.csv"

def main():
    def gui():
        global window
        window = tk.Tk()
        window.geometry("500x500")
        description = tk.Label(text="Branded Terms")
        global entry1, entry2
        entry1 = tk.Entry(window, width=100)
        button1 = tk.Button(window, text="Submit", command=get_branded_info)
        description2 = tk.Label(text="Branded ASINs")
        entry2 = tk.Entry(window, width= 100)
        description.pack()
        entry1.pack()
        description2.pack()
        entry2.pack()
        button1.pack()
        window.mainloop()

    def get_branded_info():
        global entry1, entry2
        global e1, e2
        e1 = entry1.get()
        e2 = entry2.get()
        window.destroy()

    file_path = os.getcwd()

    # Join the directory path with the file name
    st_file_path = os.path.join(file_path, 'st_report.csv')
    ad_report_file_path = os.path.join(file_path, 'ad_report.csv')
    gui()
    try:
        branded_keywords = e1
        branded_asins = e2
        # branded_keywords = input("Please enter your branded terms, separated by a comma: ")
        # branded_keywords = "boom, broom, bloom, joseph, josef, cindy, sindy"
        branded_keywords = branded_keywords.split(", ")
        # branded_asins = input("Please enter your branded ASINs, separated by a comma: ")
        # branded_asins = "b08s49fm3c, b08v1cg1gf, b08tzwfbg5, b08tzd3g7j, b08tzv54mn, b09v2bjq54, b09vvgjp4w, b09vv9nczr, b09vs1j5yn, b09vs8mml1, b09vs4p2p6, b0blw7mslt, b0bnp7n33c, b0bnp77gct, b0b9cj89fn"
        branded_asins = branded_asins.split(", ")
        calculate_overall_perfomance_metrics(st_file_path, ad_report_file_path, branded_keywords, branded_asins)

    except (FileNotFoundError, PermissionError) as error:
        print(type(error).__name__, error, sep=": ")


def calculate_overall_perfomance_metrics(st_file_path, ad_report_file_path, branded_keywords, branded_asins):
    with open(st_file_path, newline='') as f:
        reader = csv.reader(f)
        h = next(reader)
        # data = next(headers)
    df = pd.read_csv(st_file_path)
    # df['Spend'] = df['Spend'].astype(int)
    # df['7 Day Total Sales '] = df['7 Day Total Sales '].astype(int)
    # sum_spend = df["Spend"].sum()
    # sum_sales = df["7 Day Total Sales "].sum()
    
    df2 = df.replace(to_replace=np.nan, value=int(0))

    df2["Spend"].fillna(int(0))
    df2["7 Day Total Sales "].fillna(int(0))
    # df2.replace(to_replace=r'\*', value='auto', regex=True)
    
    df2["Targeting"] = df2["Targeting"].astype("str")
    df2["7 Day Total Sales "] = df2["7 Day Total Sales "].fillna(0)
    df2["Spend"] = df2["Spend"].fillna(0)
    df3 = df2.fillna(0)
    df3['7 Day Total Sales '] = df['7 Day Total Sales '].replace(np.nan, 0)
    sum_spend = df3["Spend"].sum()
    sum_sales = df3["7 Day Total Sales "].sum()
    print()
    print(f"Sum of Spend: ${sum_spend:,.2f}")
    print(f"Sum of Sales: ${sum_sales:,.2f}")
    acos = sum_spend / sum_sales * 100
    print(f"ACoS: {acos:,.2f}%")
    
   
    br_kw_auto_spend = 0
    br_kw_auto_spend_sum = 0
    br_kw_auto_sales = 0
    br_kw_auto_sales_sum = 0
    nb_kw_auto_spend = 0
    nb_kw_auto_spend_sum = 0
    nb_kw_auto_sales = 0
    nb_kw_auto_sales_sum = 0
    br_pt_auto_spend = 0 
    br_pt_auto_spend_sum = 0 
    br_pt_auto_sales = 0
    br_pt_auto_sales_sum = 0
    nb_pt_auto_spend = 0
    nb_pt_auto_spend_sum = 0
    nb_pt_auto_sales = 0
    nb_pt_auto_sales_sum = 0
    br_pt_manual_spend = 0
    br_pt_manual_spend_sum = 0
    br_pt_manual_sales = 0
    br_pt_manual_sales_sum = 0
    nb_pt_manual_spend = 0
    nb_pt_manual_spend_sum = 0
    nb_pt_manual_sales = 0
    nb_pt_manual_sales_sum = 0
    br_kw_manual_spend = 0
    br_kw_manual_spend_sum = 0
    br_kw_manual_sales = 0
    br_kw_manual_sales_sum = 0
    nb_kw_manual_spend = 0
    nb_kw_manual_spend_sum = 0
    nb_kw_manual_sales = 0
    nb_kw_manual_sales_sum = 0
    nb_pt_manual_spend = 0
    nb_pt_manual_spend_sum = 0
    nb_pt_manual_sales = 0
    nb_pt_manual_sales_sum = 0
    nb_pt_cat_manual_spend_sum = 0
    nb_pt_cat_manual_sales_sum = 0
    row_number = 1

    branded_keyword = ""
    branded_asin = ""
    nb_st_list = []
    br_st_list = []
    all_st_list = []
    all_st_kw_list = []
    all_target_list = []
    undefined_array = []

    def create_target_list():
        for target in df3["Targeting"]:
            as_str = str(target)
            all_target_list.append(as_str)
    def create_st_list():
        for st in df3["Customer Search Term"]:
            as_str = str(st)
            all_st_list.append(as_str)

    def create_kw_list():
        for target, st in zip(all_target_list, all_st_list):
            if "asin" not in target and "\*" not in target and "category" not in target:
                if "b0" not in st:
                    all_st_kw_list.append(st)
    

    def segment_st_to_br_or_nb(all_st_list, branded_keywords):
        for st in all_st_list:
            if not any(br_kw in st for br_kw in branded_keywords):
                nb_st_list.append(st)
            else:
                br_st_list.append(st)
                
    if len(branded_keywords) <= 1:
        branded_keyword = str(branded_keywords)
    if len(branded_asins) <= 1:
        branded_asin = str(branded_asins)

    str(branded_keyword)
    str(branded_asin)

    create_target_list()
    create_st_list()
    create_kw_list()
    segment_st_to_br_or_nb(all_st_list, branded_keywords)

  
    if len(branded_keywords) <= 1:
        for row in df3["Targeting"]:
            

            current_row = df.iloc[row_number - 1]
            current_row = current_row.replace(to_replace=np.nan, value=int(0))
            search_term = current_row["Customer Search Term"]
            if not isinstance(current_row, str):
                str(row)

            if "*" in row:
                if not isinstance(row, str):
                    row = str(row)

                if "asin" not in row:
                    if str(branded_keyword) in str(search_term):
                        current_row_br_kw_auto_spend = current_row["Spend"]
                        br_kw_auto_spend_sum = br_kw_auto_spend_sum + current_row_br_kw_auto_spend
                        current_row_br_kw_auto_sales = current_row["7 Day Total Sales "]
                        br_kw_auto_sales_sum = br_kw_auto_sales_sum + current_row_br_kw_auto_sales
                    else:
                        current_row_nb_kw_auto_spend = current_row["Spend"]
                        nb_kw_auto_spend_sum = nb_kw_auto_spend_sum + current_row_nb_kw_auto_spend
                        current_row_nb_kw_auto_sales = current_row["7 Day Total Sales "]
                        nb_kw_auto_sales_sum = nb_kw_auto_sales_sum + current_row_nb_kw_auto_sales 
                else:

                    if any(str(br_asin) in str(search_term) for br_asin in branded_asins):
                        current_row_br_pt_auto_spend = current_row["Spend"]
                        br_pt_auto_spend_sum = br_pt_auto_spend_sum + current_row_br_pt_auto_spend
                        current_row_br_pt_auto_sales = current_row["7 Day Total Sales "]
                        br_pt_auto_sales_sum = br_pt_auto_sales_sum + current_row_br_pt_auto_sales
                    else:
                        current_row_nb_pt_auto_spend = current_row["Spend"]
                        nb_pt_auto_spend_sum = nb_pt_auto_spend_sum + current_row_nb_pt_auto_spend
                        current_row_nb_pt_auto_sales = current_row["7 Day Total Sales "]
                        nb_pt_auto_sales_sum = nb_pt_auto_sales_sum + current_row_nb_pt_auto_sales 

            elif "asin" in row:
                if any(str(br_asin) in str(row) for br_asin in branded_asins):
                        current_row_br_pt_manual_spend = current_row["Spend"]
                        br_pt_manual_spend_sum = br_pt_manual_spend_sum + current_row_br_pt_manual_spend
                        current_row_br_pt_manual_sales = current_row["7 Day Total Sales "]
                        br_pt_manual_sales_sum = br_pt_manual_sales_sum + current_row_br_pt_manual_sales
                else:
                        current_row_nb_pt_manual_spend = current_row["Spend"]
                        nb_pt_manual_spend_sum = nb_pt_manual_spend_sum + current_row_nb_pt_manual_spend
                        current_row_nb_pt_manual_sales = current_row["7 Day Total Sales "]
                        nb_pt_manual_sales_sum = nb_pt_manual_sales_sum + current_row_nb_pt_manual_sales 
                
            elif "category=" in row:
                current_row_nb_pt_cat_manual_spend = current_row["Spend"]
                nb_pt_cat_manual_spend_sum = nb_pt_cat_manual_spend_sum + current_row_nb_pt_cat_manual_spend
                current_row_nb_pt_cat_manual_sales = current_row["7 Day Total Sales "]
                nb_pt_cat_manual_sales_sum = nb_pt_cat_manual_sales_sum + current_row_nb_pt_cat_manual_sales

            elif any(str(search_term) == br_st for br_st in br_st_list):
                current_row_br_kw_manual_spend = current_row["Spend"]
                br_kw_manual_spend_sum = br_kw_manual_spend_sum + current_row_br_kw_manual_spend
                current_row_br_kw_manual_sales = current_row["7 Day Total Sales "]
                br_kw_manual_sales_sum = br_kw_manual_sales_sum + current_row_br_kw_manual_sales


            elif any(str(nb_kw) == str(search_term) for nb_kw in nb_st_list):
                current_row_nb_kw_manual_spend = current_row["Spend"]
                nb_kw_manual_spend_sum = nb_kw_manual_spend_sum + current_row_nb_kw_manual_spend
                current_row_nb_kw_manual_sales = current_row["7 Day Total Sales "]
                nb_kw_manual_sales_sum = nb_kw_manual_sales_sum + current_row_nb_kw_manual_sales  

            elif row == "" or row == 0:
                break

            else:
                undefined_array.append(row)
                
            
            row_number = row_number + 1
    elif len(branded_asins) <= 1:
        for row in df3["Targeting"]:
            

            current_row = df.iloc[row_number - 1]
            current_row = current_row.replace(to_replace=np.nan, value=int(0))
            search_term = current_row["Customer Search Term"]
            if not isinstance(current_row, str):
                str(row)

            if "*" in row:
                if not isinstance(row, str):
                    row = str(row)

                if "asin" not in row:
                    if any(br_kw in search_term for br_kw in branded_keywords):
                        current_row_br_kw_auto_spend = current_row["Spend"]
                        br_kw_auto_spend_sum = br_kw_auto_spend_sum + current_row_br_kw_auto_spend
                        current_row_br_kw_auto_sales = current_row["7 Day Total Sales "]
                        br_kw_auto_sales_sum = br_kw_auto_sales_sum + current_row_br_kw_auto_sales
                    else:
                        current_row_nb_kw_auto_spend = current_row["Spend"]
                        nb_kw_auto_spend_sum = nb_kw_auto_spend_sum + current_row_nb_kw_auto_spend
                        current_row_nb_kw_auto_sales = current_row["7 Day Total Sales "]
                        nb_kw_auto_sales_sum = nb_kw_auto_sales_sum + current_row_nb_kw_auto_sales 
                else:

                    if branded_asin in search_term:
                        current_row_br_pt_auto_spend = current_row["Spend"]
                        br_pt_auto_spend_sum = br_pt_auto_spend_sum + current_row_br_pt_auto_spend
                        current_row_br_pt_auto_sales = current_row["7 Day Total Sales "]
                        br_pt_auto_sales_sum = br_pt_auto_sales_sum + current_row_br_pt_auto_sales
                    else:
                        current_row_nb_pt_auto_spend = current_row["Spend"]
                        nb_pt_auto_spend_sum = nb_pt_auto_spend_sum + current_row_nb_pt_auto_spend
                        current_row_nb_pt_auto_sales = current_row["7 Day Total Sales "]
                        nb_pt_auto_sales_sum = nb_pt_auto_sales_sum + current_row_nb_pt_auto_sales 

            elif "asin" in row:
                if branded_asin in search_term:
                        current_row_br_pt_manual_spend = current_row["Spend"]
                        br_pt_manual_spend_sum = br_pt_manual_spend_sum + current_row_br_pt_manual_spend
                        current_row_br_pt_manual_sales = current_row["7 Day Total Sales "]
                        br_pt_manual_sales_sum = br_pt_manual_sales_sum + current_row_br_pt_manual_sales
                else:
                        current_row_nb_pt_manual_spend = current_row["Spend"]
                        nb_pt_manual_spend_sum = nb_pt_manual_spend_sum + current_row_nb_pt_manual_spend
                        current_row_nb_pt_manual_sales = current_row["7 Day Total Sales "]
                        nb_pt_manual_sales_sum = nb_pt_manual_sales_sum + current_row_nb_pt_manual_sales 
                
            elif "category=" in row:
                current_row_nb_pt_cat_manual_spend = current_row["Spend"]
                nb_pt_cat_manual_spend_sum = nb_pt_cat_manual_spend_sum + current_row_nb_pt_cat_manual_spend
                current_row_nb_pt_cat_manual_sales = current_row["7 Day Total Sales "]
                nb_pt_cat_manual_sales_sum = nb_pt_cat_manual_sales_sum + current_row_nb_pt_cat_manual_sales

            elif any(br_kw in search_term for br_kw in branded_keywords) in search_term:
                current_row_br_kw_manual_spend = current_row["Spend"]
                br_kw_manual_spend_sum = br_kw_manual_spend_sum + current_row_br_kw_manual_spend
                current_row_br_kw_manual_sales = current_row["7 Day Total Sales "]
                br_kw_manual_sales_sum = br_kw_manual_sales_sum + current_row_br_kw_manual_sales


            elif any(nb_kw in search_term for nb_kw in nb_st_list):
                current_row_nb_kw_manual_spend = current_row["Spend"]
                nb_kw_manual_spend_sum = nb_kw_manual_spend_sum + current_row_nb_kw_manual_spend
                current_row_nb_kw_manual_sales = current_row["7 Day Total Sales "]
                nb_kw_manual_sales_sum = nb_kw_manual_sales_sum + current_row_nb_kw_manual_sales  

            elif row == "" or row == 0:
                break

            else:
                undefined_array.append(row)
                
            
            row_number = row_number + 1
    
    else: 
        for row in df3["Targeting"]:
            

            current_row = df.iloc[row_number - 1]
            current_row = current_row.replace(to_replace=np.nan, value=int(0))
            search_term = current_row["Customer Search Term"]
            if not isinstance(current_row, str):
                str(row)

            if "*" in row:
                if not isinstance(row, str):
                    row = str(row)

                if "asin" not in row:
                    if any(br_kw in search_term for br_kw in branded_keywords):
                        current_row_br_kw_auto_spend = current_row["Spend"]
                        br_kw_auto_spend_sum = br_kw_auto_spend_sum + current_row_br_kw_auto_spend
                        current_row_br_kw_auto_sales = current_row["7 Day Total Sales "]
                        br_kw_auto_sales_sum = br_kw_auto_sales_sum + current_row_br_kw_auto_sales
                    else:
                        current_row_nb_kw_auto_spend = current_row["Spend"]
                        nb_kw_auto_spend_sum = nb_kw_auto_spend_sum + current_row_nb_kw_auto_spend
                        current_row_nb_kw_auto_sales = current_row["7 Day Total Sales "]
                        nb_kw_auto_sales_sum = nb_kw_auto_sales_sum + current_row_nb_kw_auto_sales 
                else:

                    if any(br_asin in search_term for br_asin in branded_asins):
                        current_row_br_pt_auto_spend = current_row["Spend"]
                        br_pt_auto_spend_sum = br_pt_auto_spend_sum + current_row_br_pt_auto_spend
                        current_row_br_pt_auto_sales = current_row["7 Day Total Sales "]
                        br_pt_auto_sales_sum = br_pt_auto_sales_sum + current_row_br_pt_auto_sales
                    else:
                        current_row_nb_pt_auto_spend = current_row["Spend"]
                        nb_pt_auto_spend_sum = nb_pt_auto_spend_sum + current_row_nb_pt_auto_spend
                        current_row_nb_pt_auto_sales = current_row["7 Day Total Sales "]
                        nb_pt_auto_sales_sum = nb_pt_auto_sales_sum + current_row_nb_pt_auto_sales 

            elif "asin" in row:
                if any(str(br_asin) in row for br_asin in branded_asins):
                        current_row_br_pt_manual_spend = current_row["Spend"]
                        br_pt_manual_spend_sum = br_pt_manual_spend_sum + current_row_br_pt_manual_spend
                        current_row_br_pt_manual_sales = current_row["7 Day Total Sales "]
                        br_pt_manual_sales_sum = br_pt_manual_sales_sum + current_row_br_pt_manual_sales
                else:
                        current_row_nb_pt_manual_spend = current_row["Spend"]
                        nb_pt_manual_spend_sum = nb_pt_manual_spend_sum + current_row_nb_pt_manual_spend
                        current_row_nb_pt_manual_sales = current_row["7 Day Total Sales "]
                        nb_pt_manual_sales_sum = nb_pt_manual_sales_sum + current_row_nb_pt_manual_sales 
                
            elif "category=" in row:
                current_row_nb_pt_cat_manual_spend = current_row["Spend"]
                nb_pt_cat_manual_spend_sum = nb_pt_cat_manual_spend_sum + current_row_nb_pt_cat_manual_spend
                current_row_nb_pt_cat_manual_sales = current_row["7 Day Total Sales "]
                nb_pt_cat_manual_sales_sum = nb_pt_cat_manual_sales_sum + current_row_nb_pt_cat_manual_sales

            elif any(br_kw in search_term for br_kw in branded_keywords):
                current_row_br_kw_manual_spend = current_row["Spend"]
                br_kw_manual_spend_sum = br_kw_manual_spend_sum + current_row_br_kw_manual_spend
                current_row_br_kw_manual_sales = current_row["7 Day Total Sales "]
                br_kw_manual_sales_sum = br_kw_manual_sales_sum + current_row_br_kw_manual_sales


            elif any(nb_kw in search_term for nb_kw in nb_st_list):
                current_row_nb_kw_manual_spend = current_row["Spend"]
                nb_kw_manual_spend_sum = nb_kw_manual_spend_sum + current_row_nb_kw_manual_spend
                current_row_nb_kw_manual_sales = current_row["7 Day Total Sales "]
                nb_kw_manual_sales_sum = nb_kw_manual_sales_sum + current_row_nb_kw_manual_sales  

            elif row == "" or row == 0:
                break

            else:
                undefined_array.append(row)
                
            
            row_number = row_number + 1



    br_total_spend = br_kw_auto_spend_sum + br_kw_manual_spend_sum + br_pt_auto_spend_sum + br_pt_manual_spend_sum
    br_total_sales = br_kw_auto_sales_sum + br_kw_manual_sales_sum + br_pt_auto_sales_sum + br_pt_manual_sales_sum
    if br_total_sales != 0:
        br_acos = br_total_spend / br_total_sales * 100
    else:
        br_acos = 0

    nb_total_spend = nb_kw_auto_spend_sum + nb_kw_manual_spend_sum + nb_pt_auto_spend_sum + nb_pt_manual_spend_sum + nb_pt_cat_manual_spend_sum
    nb_total_sales = nb_kw_auto_sales_sum + nb_kw_manual_sales_sum+ nb_pt_auto_sales_sum + nb_pt_manual_sales_sum + nb_pt_cat_manual_sales_sum
    if nb_total_sales != 0:
        nb_acos = nb_total_spend / nb_total_sales * 100
    else:
        nb_acos = 0

    br_kw_spend = br_kw_auto_spend_sum + br_kw_manual_spend_sum
    br_kw_sales = br_kw_auto_sales_sum + br_kw_manual_sales_sum
    if br_kw_sales != 0:
        br_kw_acos = br_kw_spend / br_kw_sales * 100
    else:
        br_kw_acos = 0

    br_pt_spend = br_pt_auto_spend_sum + br_pt_manual_spend_sum
    br_pt_sales = br_pt_auto_sales_sum + br_pt_manual_sales_sum
    if br_pt_sales != 0:
        br_pt_acos = br_pt_spend / br_pt_sales * 100
    else:
        br_pt_acos = 0

    nb_kw_spend = nb_kw_auto_spend_sum + nb_kw_manual_spend_sum
    nb_kw_sales = nb_kw_auto_sales_sum + nb_kw_manual_sales_sum    
    if nb_kw_sales != 0:
        nb_kw_acos = nb_kw_spend / nb_kw_sales * 100
    else:
        nb_kw_acos = 0
    nb_pt_spend = nb_pt_auto_spend_sum + nb_pt_manual_spend_sum + nb_pt_cat_manual_spend_sum
    nb_pt_sales = nb_pt_auto_sales_sum + nb_pt_manual_sales_sum + nb_pt_cat_manual_sales_sum
    if nb_pt_sales != 0:
        nb_pt_acos = nb_pt_spend / nb_pt_sales * 100
    else:
        nb_pt_acos = 0
    
    
    print()
    print(f"BR Spend: {br_total_spend:,.2f}")
    print(f"BR Sales: {br_total_sales:,.2f}")
    print(f"BR ACoS: {br_acos:,.2f}%")
    print()
    print(f"NB Spend: {nb_total_spend:,.2f}")
    print(f"NB Sales: {nb_total_sales:,.2f}")
    print(f"NB ACoS: {nb_acos:,.2f}%")
    print()
    print(f"BR KW Spend: {br_kw_spend:,.2f}")
    print(f"BR KW Sales: {br_kw_sales:,.2f}")
    print(f"BR KW ACoS: {br_kw_acos:,.2f}%")
    print()
    print(f"BR PT Spend: {br_pt_spend:,.2f}")
    print(f"BR PT Sales: {br_pt_sales:,.2f}")
    print(f"BR PT ACoS: {br_pt_acos:,.2f}%")
    print()
    print(f"NB KW Spend: {nb_kw_spend:,.2f}")
    print(f"NB KW Sales: {nb_kw_sales:,.2f}")
    print(f"NB KW ACoS: {nb_kw_acos:,.2f}%")
    print()
    print(f"NB PT Spend: {nb_pt_spend:,.2f}")
    print(f"NB PT Sales: {nb_pt_sales:,.2f}")
    print(f"NB PT ACoS: {nb_pt_acos:,.2f}%")

   

    data1 = ["Total Spend", round(sum_spend, 2)]
    data2 = ["Ad Sales Sales", round(sum_sales, 2)]
    data3 = ["ACoS", round(acos, 2)]
    data4 = ""
    data5 = ["Branded Spend", round(br_total_spend, 2)]
    data6 = ["Branded Sales", round(br_total_sales, 2)]
    data7 = ["Branded ACoS", round(br_acos, 2)]
    data8 = ""
    data9 = ["Non-Branded Spend", round(nb_total_spend, 2)]
    data10 = ["Non-Branded Sales", round(nb_total_sales, 2)]
    data11 = ["Non-Branded ACoS", round(nb_acos, 2)]
    data12 = [""]
    data13= ["Branded KW Spend", round(br_kw_spend, 2)]
    data14= ["Branded KW Sales", round(br_kw_sales, 2)]
    data15= ["Branded KW ACoS", round(br_kw_acos, 2)]
    data16 = [""]
    data17= ["Branded PT Spend", round(br_pt_spend, 2)]
    data18= ["Branded PT Sales", round(br_pt_sales, 2)]
    data19= ["Branded PT ACoS", round(br_pt_acos, 2)]
    data20 = [""]
    data21= ["Non-Branded KW Spend", round(nb_kw_spend, 2)]
    data22= ["Non-Branded KW Sales", round(nb_kw_sales, 2)]
    data23= ["Non-Branded KW ACoS", round(nb_kw_acos, 2)]
    data24 = [""]
    data25= ["Non-Branded PT Spend", round(nb_pt_spend, 2)]
    data26= ["Non-Branded PT Sales", round(nb_pt_sales, 2)]
    data27= ["Non-Branded PT ACoS", round(nb_pt_acos, 2)]

    
    with open("ad_report.csv", "w") as report:
        report = csv.writer(report)
        report.writerow(data1)
        report.writerow(data2)
        report.writerow(data3)
        report.writerow(data4)
        report.writerow(data5)
        report.writerow(data6)
        report.writerow(data7)
        report.writerow(data8)
        report.writerow(data9)
        report.writerow(data10)
        report.writerow(data11)
        report.writerow(data12)
        report.writerow(data13)
        report.writerow(data14)
        report.writerow(data15)
        report.writerow(data16)
        report.writerow(data17)
        report.writerow(data18)
        report.writerow(data19)
        report.writerow(data20)
        report.writerow(data21)
        report.writerow(data22)
        report.writerow(data23)
        report.writerow(data24)
        report.writerow(data25)
        report.writerow(data26)
        report.writerow(data27)
        
    subprocess.call(["open", ad_report_file_path])
    # open("ad_report.csv")  

if __name__ == "__main__":
    main()

