# import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, \
# NoSuchElementException, ElementClickInterceptedException



# # options = Options()
# # options.add_argument("start-maximized")
# # driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:/chrome_driver/chromedriver.exe')
# # driver.get('https://www.google.co.in')


# """ Configure the chromedriver with your Local Drive"""
# # chrome_options = webdriver.ChromeOptions()
# # chrome = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)

# options = webdriver.ChromeOptions()
# # options.add_argument('--no-sandbox')
# options.add_argument("headless")
# # driver = webdriver.Chrome('C:/chrome_driver/chromedriver.exe')
# driver = webdriver.Chrome('C:/chrome_driver/chromedriver.exe', options=options)




# def close_browser():
    
#     driver.close()
    
    
# """ Login and Search with cerpac Numbers """
# def search_by_cerpac(datas):
#     try:
#         driver.maximize_window()  
#         driver.get("http://knowyourimmigrationstatus.ng/KnowStatusCerpac.aspx")
#         init = driver.current_url  
#         inputElement = driver.find_element_by_id("ContentPlaceHolder1_txtcerpac")
#         inputElement.send_keys(datas)
#         driver.find_element_by_id("ContentPlaceHolder1_btnchk").click()
#         time.sleep(5)
#         imit = driver.current_url
#         if init != imit:
#             print('Login successful !')
#     except:
#         print('Login not Successful! ') 
        
        
# def verify_company(company):
#     try:
#         driver.maximize_window()  
#         driver.get("https://ecitibiz.interior.gov.ng/Expatriate/CompanyVerification")
#         init = driver.current_url  
#         inputElement = driver.find_element_by_id("txtCompanyName")
#         inputElement.send_keys(company)
#         driver.find_element_by_id("btnSearch").click()
#         time.sleep(5)
#         imit = driver.current_url
#         if init != imit:
#             print('Login successful !')
#     except:
#         print('Login not Successful! ') 
        
# """ Login and Search with Form Numbers"""
# def search_by_form(form):
#     try:        
#         driver.maximize_window()  
#         driver.get("http://knowyourimmigrationstatus.ng/FormStatusDetails.aspx")                 
#         inputElement = driver.find_element_by_id("ContentPlaceHolder1_txtform")
#         inputElement.send_keys(form)
#         driver.find_element_by_id("ContentPlaceHolder1_btnchk").click()
#         time.sleep(5)
#         try:
#             form_data = driver.find_elements_by_xpath("//div[@id='ContentPlaceHolder1_formdetail']/table[1]/tbody/tr/td")
#             time.sleep(3)
#             form_info = []
#             for i in form_data:
#                 if i.text!=" " and ":" not in i.text:                    
#                     form_info.append(i.text)                                 
#                     i.text+''          
#             return form_info
#             print('Login Successful ! ') 
#         except NoSuchElementException:
#             print('Login not Successful! ') 
#     except:
#         print('Login not Successful! ') 



# def get_cerpac_details():
#     tableData = driver.find_elements_by_xpath("//form[@id='form1']/center[1]/div[2]/div[2]/div[3]/table[1]/tbody[1]/tr/td")
#     cerpac =[]
#     for i in tableData:    
#         if i.text!="" and ":" not in i.text:
#             cerpac.append(i.text)         
#             i.text+''
#     return cerpac

   

# def get_applicant_info():
#     applicant_data = driver.find_elements_by_xpath("//form[@id='form1']/center[1]/div[2]/div[2]/div[2]/table[1]/tbody/tr/td")
#     applicant_info = []
#     for i in applicant_data:
#         if i.text!="" and ":" not in i.text:         
#             applicant_info.append(i.text)
#             i.text+ ''
#     return applicant_info

  
# def get_status_details():    
#     statusData = driver.find_elements_by_xpath("//form[@id='form1']/center[1]/div[2]/div[2]/div[4]/table[1]/tbody/tr/td")
#     status_list = []
#     for i in statusData:
#         if i.text!="" and ":" not in i.text:
#             status_list.append(i.text)
#             i.text+ ''
#     return status_list


# def verify_quota(rcc_number, eq_number):    
#     driver.maximize_window()  
#     driver.get("https://ecitibiz.interior.gov.ng/Expatriate/ExpatriateApprovalSearch")
#     url = driver.current_url
#     try:        
#         inputElement = driver.find_element_by_id("RCNumber")
#         inputElement.send_keys(rcc_number)
#         driver.find_element_by_id("btnSearch").click()
#         inputElement = driver.find_element_by_css_selector("input[type='search']")
#         inputElement.send_keys(eq_number)
#         time.sleep(2) # wait for 2 seconds
#         try:
#             listings_table = driver.find_element_by_id('myTable')
#             listings_table_rows = listings_table.find_elements_by_tag_name('td')
#             store_quota_details =[] #create a new list            
#             for i in listings_table_rows:
#                 store_quota_details.append(i.text)
#                 i.text+ ''
#             print('Login successful ....')  
#             return store_quota_details
#         except NoSuchElementException:
#             print('Error: No such element')
#             print('Login not successful .............')
#     except NoSuchElementException:
#         print('Error: No such element')         
#         print('Login not successful .............')     


# # # """ test the functions"""
# # company = 'MULTIPRO CONSUMER PRODUCTS LIMITED'
# # form='AB106623'
# # datas ='AB133121'
# # verify_company(company)
# # # time.sleep(1)
# # close_browser()

