import re
from robobrowser import RoboBrowser

browser = RoboBrowser()
browser.open('https://click2win.settrade.com/LoginRepOnRole.jsp?txtLogin=crawler001&txtPassword=crawler001&txtSecureKey=NONE&txtDefaultPage=%2FSETClick2WIN%2FSelectUserLeague.jsp&txtLoginPage=SETClick2WIN/index.jsp&txtBrokerId=089&txtSystem=ITP&txtRole=INTERNET&tmpUsername=&tmpPassword=')
form = browser.get_forms()[0]
browser.submit_form(form)
form = browser.get_forms()[0]
form = browser.get_forms()[0]
browser.submit_form(form)

browser.open('https://click2win.settrade.com//realtime/streaming5/flash/StreamingPage.jsp')
print browser.select('html')[0]