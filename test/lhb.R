lhb-deploy.R

setwd("~/workspace/ml-r/lhb")
source("prepare.R")

dw <- dwConn_ora()
LHB <-
  dbGetQuery(
    dw,
    "SELECT NVL(A.TRX_DATE,B.TRX_DATE) TRX_DATE,
       A.T1_INVEST_AMOUNT,
       B.T1_OUT_AMOUNT,
       G.T28_INVEST_AMOUNT,
       H.T28_OUT_AMOUNT,
       E.T14_INVEST_AMOUNT,
       F.T14_OUT_AMOUNT
FROM
    ( SELECT TO_CHAR(CMN.TRX_DATE,'YYYY-MM-DD') TRX_DATE,
             SUM(CMN.AMOUNT) T1_INVEST_AMOUNT
     FROM ODL.BUS_FUND_BUY_REQUEST CMN
     LEFT JOIN ODL.K_BUS_FUND_LOAN_REQUEST B ON CMN.EX_PROD_CODE=B.THIRD_COMPANY_CODE
     WHERE B.PRODUCT_CATEGORY=801
         AND B.LOCK_DAY_COUNT=0
         AND CMN.STATUS='SUCCESS'
         AND TO_CHAR(CMN.TRX_DATE,'YYYY-MM-DD') > = '2015-01-01'
     GROUP BY TO_CHAR(CMN.TRX_DATE,'YYYY-MM-DD') ) A FULL
JOIN
    (SELECT TRX_DATE,
            SUM(AMOUNT) T1_OUT_AMOUNT
     FROM
         ( SELECT FUND_DATE,
                  SUBSTR(FUND_DATE,9),
                  TO_CHAR(TO_DATE(SUBSTR(FUND_DATE,1,8),'YYYYMMDD'),'YYYY-MM-DD') TRX_DATE,
                  AMOUNT
          FROM ODL.BUS_FUND_WITHDRAW_RECORD A
          LEFT JOIN ODL.CMN_PRODUCTS B ON A.PRODUCT_ID=B.PRODUCT_ID
          LEFT JOIN ODL.K_BUS_FUND_LOAN_REQUEST C ON B.CODE=C.PRODUCT_CODE
          WHERE C.PRODUCT_CATEGORY=801
              AND C.LOCK_DAY_COUNT=0
              AND ((SUBSTR(FUND_DATE,9)='-1-1'
                    AND TYPE=1)
                   OR TYPE=2)
              AND TO_DATE(SUBSTR(FUND_DATE,1,8),'YYYY-MM-DD') > = to_date('2015-01-01','YYYY-MM-DD') )
     GROUP BY TRX_DATE ) B ON A.TRX_DATE=B.TRX_DATE FULL
JOIN
    ( SELECT TO_CHAR(CMN.TRX_DATE,'YYYY-MM-DD') TRX_DATE,
             SUM(CMN.AMOUNT) T28_INVEST_AMOUNT
     FROM ODL.BUS_FUND_BUY_REQUEST CMN
     LEFT JOIN ODL.K_BUS_FUND_LOAN_REQUEST B ON CMN.EX_PROD_CODE=B.THIRD_COMPANY_CODE
     WHERE CMN.STATUS='SUCCESS'
         AND B.PRODUCT_CATEGORY=801
         AND B.LOCK_DAY_COUNT=28
         AND TO_CHAR(CMN.TRX_DATE,'YYYY-MM-DD') > = '2015-01-01'
     GROUP BY TO_CHAR(CMN.TRX_DATE,'YYYY-MM-DD') ) G ON G.TRX_DATE=A.TRX_DATE FULL
JOIN
    (SELECT TRX_DATE,
            SUM(AMOUNT) T28_OUT_AMOUNT
     FROM
         ( SELECT FUND_DATE,
                  SUBSTR(FUND_DATE,9),
                  TO_CHAR(TO_DATE(SUBSTR(FUND_DATE,1,8),'YYYYMMDD'),'YYYY-MM-DD') TRX_DATE,
                  AMOUNT
          FROM ODL.BUS_FUND_WITHDRAW_RECORD A
          LEFT JOIN ODL.CMN_PRODUCTS B ON A.PRODUCT_ID=B.PRODUCT_ID
          LEFT JOIN ODL.K_BUS_FUND_LOAN_REQUEST C ON B.CODE=C.PRODUCT_CODE
          WHERE C.PRODUCT_CATEGORY=801
              AND C.LOCK_DAY_COUNT=28
              AND((SUBSTR(FUND_DATE,9)='-1-1'
                   AND TYPE=1)
                  OR TYPE=2)
              AND TO_DATE(SUBSTR(FUND_DATE,1,8),'YYYY-MM-DD') > = to_date('2015-01-01','YYYY-MM-DD') )
     GROUP BY TRX_DATE) H ON A.TRX_DATE=H.TRX_DATE FULL
JOIN
    (SELECT TO_CHAR(CMN.TRX_DATE,'YYYY-MM-DD') TRX_DATE,
            SUM(CMN.AMOUNT) T14_INVEST_AMOUNT
     FROM BUS_FUND_BUY_REQUEST CMN
     LEFT JOIN ODL.K_BUS_FUND_LOAN_REQUEST B ON CMN.EX_PROD_CODE=B.THIRD_COMPANY_CODE
     WHERE B.PRODUCT_CATEGORY=801
         AND B.LOCK_DAY_COUNT=14
         AND CMN.STATUS='SUCCESS'
         AND TO_CHAR(CMN.TRX_DATE,'YYYY-MM-DD') > = '2015-01-01'
     GROUP BY TO_CHAR(CMN.TRX_DATE,'YYYY-MM-DD')) E ON A.TRX_DATE=E.TRX_DATE FULL
JOIN
    (SELECT TRX_DATE,
            SUM(AMOUNT) T14_OUT_AMOUNT
     FROM
         (SELECT TO_CHAR(TO_DATE(SUBSTR(FUND_DATE,1,8),'YYYYMMDD'),'YYYY-MM-DD') TRX_DATE,
                 AMOUNT
          FROM BUS_FUND_WITHDRAW_RECORD A
          LEFT JOIN CMN_PRODUCTS B ON A.PRODUCT_ID=B.PRODUCT_ID
          LEFT JOIN ODL.K_BUS_FUND_LOAN_REQUEST C ON B.CODE=C.PRODUCT_CODE
          WHERE C.PRODUCT_CATEGORY=801
              AND C.LOCK_DAY_COUNT=14
              AND((SUBSTR(FUND_DATE,9)='-1-1'
                   AND TYPE=1)
                  OR TYPE=2)
              AND SUBSTR(FUND_DATE,1,8) >= '20150101')
     GROUP BY TRX_DATE) F ON A.TRX_DATE=F.TRX_DATE
ORDER BY TRX_DATE",
    bulk_read = 100000L
  )
dbDisconnect(dw)

names(LHB) <- c("RD", "T1SG", "T1SH", "T28SG", "T28SH", "T14SG", "T14SH")
LHB_T1 <- LHB %>%
  mutate(Date = as.Date(RD),
         SH = T1SH,
         SG = T1SG) %>%
  filter(Date >= '2015-08-20') %>%
  select(Date, SH, SG) 

LHB_T14 <- LHB %>%
  mutate(Date = as.Date(RD),
         SH = T14SH,
         SG = T14SG) %>%
  filter(Date >= '2015-08-20') %>%
  select(Date, SH, SG) 

LHB_T28 <- LHB %>%
  mutate(Date = as.Date(RD),
         SH = T28SH,
         SG = T28SG) %>%
  filter(Date >= '2015-08-20') %>%
  select(Date, SH, SG)

#'==============================================================================
#' 加入未来7天的时间
future_start_date <- as.Date(Sys.Date())
future_end_date <- as.Date(Sys.Date() + 6)

futureDaySales <- data.frame(date = seq(future_start_date, future_end_date, by = 1),SH = NA,SG = NA) %>% 
  mutate(Date = as.Date(date)) %>%
  select(Date,SH,SG)
print(futureDaySales)

LHB_T1 <- LHB_T1 %>% rbind(futureDaySales)
LHB_T14 <- LHB_T14 %>% rbind(futureDaySales)
LHB_T28 <- LHB_T28 %>% rbind(futureDaySales)

#===============================================================================
lhbt1sg <- LHB_T1 %>% select(Date, SG) %>% mutate(realSales = SG)
betat1sg <- 0.8
xgb_features_t1sg <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

lhbt1sh <- LHB_T1 %>% select(Date, SH) %>% rename(realSales = SH)
betat1sh <- 0.8
xgb_features_t1sh <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

lhbt14sg <- LHB_T14 %>% select(Date, SG) %>% rename(realSales = SG)
betat14sg <- 1.0
xgb_features_t14sg <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

lhbt14sh <- LHB_T14 %>% select(Date, SH) %>% rename(realSales = SH)
betat14sh <- 1.0
xgb_features_t14sh <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

lhbt28sg <- LHB_T28 %>% select(Date, SG) %>% rename(realSales = SG)
betat28sg <- 0.5
xgb_features_t28sg <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

lhbt28sh <- LHB_T28 %>% select(Date, SH) %>% rename(realSales = SH)
betat28sh <- 0.5
xgb_features_t28sh <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

#' =============================================================================
#' write data to DB
#' =============================================================================
writeToDB <- function(res,type){
  ora <- dwConn_ora()
  
  predict_exe_date = format(Sys.Date(), "%Y%m%d")
  type <- paste("'",type,"'",sep = "")
  for (i in 1:7)
  {
    sql <-
      paste(
        "insert into RDLDATA.SALES_PREDICTION (ID,PREDICT_EXE_DATE,TARGET_DATE,PREDICT_CATEGORY,AMOUNT,CREATED_AT,CREATED_BY,UPDATED_AT,UPDATED_BY)
           values (RDLDATA.SEQ_SALES_PREDICTION.NEXTVAL,",predict_exe_date,",",format(res$date, "%Y%m%d")[i],",",type,",",res$guess[i],",","SYSDATE,'R',SYSDATE,'R')",sep = "")
    print(sql)
    
    rs <- dbSendQuery(ora, sql)
  }
  dbCommit(ora)
  dbDisconnect(ora)
  print(paste("complete sales prediction", Sys.time()))
}

lhb_new_t1sg <- prepareData(betat1sg, lhbt1sg)
t1sgres <- trainingmodelloop(lhb_new_t1sg, xgb_features_t1sg, "t1sg")
writeToDB(t1sgres,"t1sg")
lhb_new_t1sh <- prepareData(betat1sh, lhbt1sh)
t1shres <- trainingmodelloop(lhb_new_t1sh, xgb_features_t1sh, "t1sh")
writeToDB(t1shres,"t1sh")

lhb_new_t14sg <- prepareData(betat14sg, lhbt14sg)
t14sgres <- trainingmodelloop(lhb_new_t14sg, xgb_features_t14sg, "t14sg")
writeToDB(t14sgres,"t14sg")
lhb_new_t14sh <- prepareData(betat14sh, lhbt14sh)
t14shres <- trainingmodelloop(lhb_new_t14sh, xgb_features_t14sh, "t14sh")
writeToDB(t14shres,"t14sh")

lhb_new_t28sg <- prepareData(betat28sg, lhbt28sg)
t28sgres <- trainingmodelloop(lhb_new_t28sg, xgb_features_t28sg, "t28sg")
writeToDB(t28sgres,"t28sg")
lhb_new_t28sh <- prepareData(betat28sh, lhbt28sh)
t28shres <- trainingmodelloop(lhb_new_t28sh, xgb_features_t28sh, "t28sh")
writeToDB(t28shres,"t28sh")










































main.R
#1022060617418
library(Ckmeans.1d.dp)

setwd("~/workspace/ml-r/lhb")

source("prepare.R")

#=============================================================================
#数据特点：周234发起的申请周345确认，周5发起的下周1确认，周671发起的下周2确认
#=============================================================================
LHB_T1 <-
  read.csv("./lhb-data/lhb-shengou-shuhui-faqi-20150101.csv", as.is = TRUE) %>%
  mutate(Date = as.Date(日期), SH=T.1赎回, SG=T.1申购) %>%
  filter(Date >= '2015-08-20') %>%
  select(Date, SH, SG) 

LHB_T14 <-
  read.csv("./lhb-data/lhb-t14.csv", as.is = TRUE) %>%
  mutate(Date = as.Date(日期), SH=T.14赎回, SG=T.14申购) %>%
  filter(Date >= '2015-09-01') %>%
  select(Date, SH, SG) 

LHB_T28 <-
  read.csv("./lhb-data/lhb-shengou-shuhui-faqi-20150101.csv", as.is = TRUE) %>%
  mutate(Date = as.Date(日期), SH=T.28赎回, SG=T.28申购) %>%
  filter(Date >= '2015-08-20') %>%
  select(Date, SH, SG) 

#===============================================================================
lhbt1sg <- LHB_T1 %>% select(Date, SG) %>% mutate(realSales = SG)
betat1sg <- 0.8
xgb_features_t1sg <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

lhbt1sh <- LHB_T1 %>% select(Date, SH) %>% rename(realSales = SH)
betat1sh <- 0.8
xgb_features_t1sh <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

lhbt14sg <- LHB_T14 %>% select(Date, SG) %>% rename(realSales = SG)
betat14sg <- 1.0
xgb_features_t14sg <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

lhbt14sh <- LHB_T14 %>% select(Date, SH) %>% rename(realSales = SH)
betat14sh <- 1.0
xgb_features_t14sh <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

lhbt28sg <- LHB_T28 %>% select(Date, SG) %>% rename(realSales = SG)
betat28sg <- 0.5
xgb_features_t28sg <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

lhbt28sh <- LHB_T28 %>% select(Date, SH) %>% rename(realSales = SH)
betat28sh <- 0.5
xgb_features_t28sh <-
  c(
    "MDay",
    "Month",
    "Year",
    "WeekOfYear",
    "IsHolidays",
    "DayOfWeek1",
    "DayOfWeek2",
    "DayOfWeek3",
    "DayOfWeek4",
    "DayOfWeek5",
    "DayOfWeek6",
    "DayOfWeek7",
    "Last1WeekDay",
    "Last2WeekDay"
  )

lhb_new_t1sg <- prepareData(betat1sg, lhbt1sg)
t1sg <- trainingmodelloop(lhb_new_t1sg, xgb_features_t1sg, "t1sg")
cat(sprintf("\nt1sg error=%f\n", rmspe_basic(t1sg$guess,t1sg$real)))
lhb_new_t1sh <- prepareData(betat1sh, lhbt1sh)
t1sh <- trainingmodelloop(lhb_new_t1sh, xgb_features_t1sh, "t1sh")
cat(sprintf("\nt1sh error=%f\n", rmspe_basic(t1sh$guess,t1sh$real)))
a <- t1sg$real - t1sh$real
b <- t1sg$guess - t1sh$guess
print(a)
print(b)

lhb_new_t14sg <- prepareData(betat14sg, lhbt14sg)
t14sg <- trainingmodelloop(lhb_new_t14sg, xgb_features_t14sg, "t14sg")
cat(sprintf("\nt14sg error=%f\n", rmspe_basic(t14sg$guess,t14sg$real)))
lhb_new_t14sh <- prepareData(betat14sh, lhbt14sh)
t14sh <- trainingmodelloop(lhb_new_t14sh, xgb_features_t14sh, "t14sh")
cat(sprintf("\nt14sh error=%f\n", rmspe_basic(t14sh$guess,t14sh$real)))
a <- t14sg$real - t14sh$real
b <- t14sg$guess - t14sh$guess
print(a)
print(b)
# print(t14sg$real-t14sg$guess)
# print(t14sh$real-t14sh$guess)
# print(rmspe_basic(b,a))

lhb_new_t28sg <- prepareData(betat28sg, lhbt28sg)
t28sg <- trainingmodelloop(lhb_new_t28sg, xgb_features_t28sg, "t28sg")
cat(sprintf("\nt28sg error=%f\n", rmspe_basic(t28sg$guess,t28sg$real)))
lhb_new_t28sh <- prepareData(betat28sh, lhbt28sh)
t28sh <- trainingmodelloop(lhb_new_t28sh, xgb_features_t28sh, "t28sh")
cat(sprintf("\nt28sh error=%f\n", rmspe_basic(t28sh$guess,t28sh$real)))
a <- t28sg$real - t28sh$real
b <- t28sg$guess - t28sh$guess
print(a)
print(b)
# print(t28sg$real-t28sg$guess)
# print(t28sh$real-t28sh$guess)
# print(rmspe_basic(b,a))



































mainplot.R

setwd("~/workspace/ml-r/lhb")


LHB_T1 <-
  read.csv("./lhb-data/lhb-shengou-shuhui-faqi-20150101.csv", as.is = TRUE) %>%
  mutate(Date = as.Date(日期), SH=T.1赎回, SG=T.1申购) %>%
  filter(Date >= '2015-11-15') %>%
  select(Date, SH, SG) 

LHB_T28 <-
  read.csv("./lhb-data/lhb-shengou-shuhui-faqi-20150101.csv", as.is = TRUE) %>%
  mutate(Date = as.Date(日期), SH=T.28赎回, SG=T.28申购) %>%
  filter(Date >= '2015-08-20') %>%
  select(Date, SH, SG)

LHB_T14 <-
  read.csv("./lhb-data/lhb-t14.csv", as.is = TRUE) %>%
  mutate(Date = as.Date(日期), SH=T.14赎回, SG=T.14申购) %>%
  filter(Date >= '2015-09-01') %>%
  select(Date, SH, SG) 
library(ggplot2)
p <-
  ggplot(
    data = LHB_T14,
    mapping = aes(x = LHB_T14$Date,
                  y = log(LHB_T14$SH)),
    group = 1
  )
p + geom_line()


library(tseries)
adf.test(log(LHB_T14$SG))


p <-
  ggplot(
    data = LHB_T14,
    mapping = aes(x = LHB_T14$Date,
                  y = log(LHB_T14$SG)),
    group = 1
  )
p + geom_line()

# #画图查看数据形状
library(ggplot2)
p <-
  ggplot(
    data = LHB_T1,
    mapping = aes(x = LHB_T1$Date,
                  y = log(LHB_T1$SH)),
    group = 1
  )
p + geom_line()

p <-
  ggplot(
    data = LHB_T1,
    mapping = aes(x = LHB_T1$Date,
                  y = LHB_T1$SH),
    group = 1
  )
p + geom_line()

p <-
  ggplot(
    data = LHB_T28,
    mapping = aes(x = LHB_T28$Date,
                  y = log(LHB_T28$SG)),
    group = 1
  )
p + geom_line()

p <-
  ggplot(
    data = LHB_T28,
    mapping = aes(x = LHB_T28$Date,
                  y = log(LHB_T28$SH)),
    group = 1
  )
p + geom_line()


































prepare.R

library(forecast)
library(dplyr)
library(DataCombine)
library(lubridate)
library(xgboost)
library(lazyeval)


library(xts)
library(data.table)

#根据数据框的某一列排序
sort.data.frame <- function(x,
                            decreasing = FALSE,
                            by = 1,
                            ...) {
  f <- function(...)
    order(..., decreasing = decreasing)
  i <- do.call(f, x[by])
  x[i, , drop = FALSE]
}


#计算过去N周内对应工作日的中位数
make_week_medians <- function(data, weeks) {
  res <- select(data, Date, Sales)
  for (week in weeks) {
    rdata <- list()
    for (dow in 1:7) {
      dowSales <-
        data %>% filter(DayOfWeek == dow) %>% select(Date, Sales)
      dowSales_xts <-
        xts(lag(dowSales$Sales), as.Date(dowSales$Date)) %>% na.fill("extend") %>% rollmedian(week, fill = NA, align = c("right")) %>% na.fill("extend")
      
      rdata[[dow]] <-
        data.frame(as.Date(index(dowSales_xts)), dowSales_xts, row.names = NULL)
    }
    windowMedian <- rbindlist(rdata)
    names(windowMedian) <-
      c("Date", paste("Last", week, "WeekMedian", sep = ""))
    res <- left_join(res, windowMedian, by = "Date", copy = TRUE)
  }
  res <- select(res,-Sales)
  res
}


#计算过去N天的销售平均值
ndays_mean <- function(data, width) {
  res <- select(data, Date)
  for (dow in width) {
    dowSales <- data %>% select(Date, Sales)
    #dowSales_xts <-
    #  xts(lag(dowSales$Sales), as.Date(dowSales$Date)) %>% na.fill("extend") %>% rollmean(dow, fill = NA, align = c("right")) %>% na.fill("extend")
    
    w <- rep(1, dow)
    #w <- seq(from=2, to=1, by=-1/(dow-1))
    w <- w / sum(w)
    dowSales_xts <-
      xts(lag(dowSales$Sales), as.Date(dowSales$Date)) %>% na.fill("extend") %>% rollapply(dow, function(x)
        weighted.mean(x, w = w), fill = NA, align = c("right")) %>% na.fill("extend")
    
    dowSales_xts <-
      data.frame(as.Date(index(dowSales_xts)), dowSales_xts, row.names = NULL)
    names(dowSales_xts) <-
      c("Date", paste("Last", dow, "DaysMean", sep = ""))
    res <- left_join(res, dowSales_xts, by = "Date", copy = TRUE)
  }
  res
}


#计算过去N天的销售平均值
ndaysincome_mean <- function(data, width) {
  res <- select(data, Date)
  for (dow in width) {
    dowSales <- data %>% select(Date, Income)
    w <- rep(1, dow)
    #w <- seq(from=2, to=1, by=-1/(dow-1))
    w <- w / sum(w)
    dowSales_xts <-
      xts(lag(dowSales$Income), as.Date(dowSales$Date)) %>% na.fill("extend") %>% rollapply(dow, function(x)
        weighted.mean(x, w = w), fill = NA, align = c("right")) %>% na.fill("extend")
    
    dowSales_xts <-
      data.frame(as.Date(index(dowSales_xts)), dowSales_xts, row.names = NULL)
    names(dowSales_xts) <-
      c("Date", paste("Last", dow, "DaysIncomeMean", sep = ""))
    res <- left_join(res, dowSales_xts, by = "Date", copy = TRUE)
  }
  res
}

makeNweekDay <- function(data, weeks) {
  res <- select(data, Date, Sales)
  for (week in weeks) {
    rdata <- list()
    for (dow in 1:7) {
      dowSales <-
        data %>% filter(DayOfWeek == dow) %>% select(Date, Sales)
      dowSales_xts <-
        xts(lag(dowSales$Sales, week), as.Date(dowSales$Date)) %>% na.fill("extend")
      
      rdata[[dow]] <-
        data.frame(as.Date(index(dowSales_xts)), dowSales_xts, row.names = NULL)
    }
    windowMedian <- rbindlist(rdata)
    names(windowMedian) <-
      c("Date", paste("Last", week, "WeekDay", sep = ""))
    res <- left_join(res, windowMedian, by = "Date", copy = TRUE)
  }
  res <- select(res,-Sales)
  res
}

#用节假日的数据生成节假日前后一周的数据，用来对目标数据打标签
generateNdaysTagNearHoliday <-
  function(dateVector,
           BeforeOrNot = TRUE,
           days = c(1, 2, 3, 4, 5)) {
    res <- c()
    if (BeforeOrNot) {
      for (i in dateVector) {
        res <- append(res, as.Date(i) - days)
      }
    } else{
      for (i in dateVector) {
        res <- append(res, as.Date(i) + days)
      }
    }
    res
  }

#将周671的数据合并在一起作为周1总的发起
combine671Data <- function(data) {
  res <- select(data, Date, SG, SH) %>%
    filter(((wday(Date) + 5) %% 7 + 1) >= 2 &
             ((wday(Date) + 5) %% 7 + 1) <= 5)
  tempdata <- select(data, Date, SG, SH) %>%
    slide(Var = "SG",
          slideBy = -1,
          NewVar = "SG1") %>%
    slide(Var = "SG",
          slideBy = -2,
          NewVar = "SG2") %>%
    slide(Var = "SH",
          slideBy = -1,
          NewVar = "SH1") %>%
    slide(Var = "SH",
          slideBy = -2,
          NewVar = "SH2")
  tempdata <- filter(tempdata, ((wday(Date) + 5) %% 7 + 1) == 1) %>%
    mutate(NEWSG = SG + SG1 + SG2, NEWSH = SH + SH1 + SH2) %>%
    rename(SG = NEWSG, SH = NEWSH)
  res <-
    res %>% bind_rows(tempdata) %>% sort.data.frame(by = "Date") %>% select(Date, SG, SH)
  res
}


library(xgboost)
library(dplyr)


predict_xgboost <- function(train, test, eval_function,
                            validate = NULL, ...) {
  set.seed(1999)
  dtrain <- xgb.DMatrix(data.matrix(select(train,-Sales,-Date)),
                        label = train$Sales,
                        missing = NA)
  dtest <-
    xgb.DMatrix(data.matrix(select(test,-Sales,-Date)), missing = NA)
  
  if (!is.null(validate)) {
    watchlist <- list(validate = xgb.DMatrix(
      data.matrix(select(validate,-Sales,-Date)),
      label = validate$Sales,
      missing = NA
    ))
  } else {
    watchlist <- list(train = dtrain)
  }
  
  fit <- xgb.train(
    data = dtrain,
    feval = eval_function,
    early.stop.round = 100,
    maximize = FALSE,
    watchlist = watchlist,
    verbose = 1,
    print.every.n = 100,
    ...
  )
  pred <- predict(fit, dtest)
  predicted <- mutate(test, PredictedSales = pred)
  list(predicted = predicted,
       fit = fit,
       dtrain = dtrain)
}

makeNdaysSalesWithHW <- function(x, h)
{
  train.end <- time(x)[length(x) - h]
  test.start <- time(x)[length(x) - h + 1]
  train <- window(x, end = train.end)
  test <- window(x, start = test.start)
  
  rainseriesforecasts <- HoltWinters(train)
  rainseriesforecasts2 <-
    forecast.HoltWinters(rainseriesforecasts, h = h)
  
  return(as.vector(rainseriesforecasts2$mean))
}


make_fold_range <-
  function(train,
           validlength = 14,
           predictlength = 7) {
    total <- nrow(train)
    
    last_train_index <- total - validlength - predictlength
    
    first_valid_index <- last_train_index + 1
    last_valid_index <- last_train_index + validlength
    
    
    first_predict_index <- last_valid_index + 1
    last_predict_index <- total
    
    train_set <- train[1:last_train_index,]
    valid_set <- train[first_valid_index:last_valid_index,]
    test_set <- train[first_predict_index:last_predict_index,]
    
    #这里先使用时间序列模型对预测时间段内的数据进行第一次预测
    FirstTemp <-
      makeNdaysSalesWithHW(ts(as.vector(train_set$Sales), frequency = 7),
                           h = (last_predict_index - first_predict_index + 1))
    test_set$First <- FirstTemp
    
    list(train = train_set,
         test = test_set,
         actual = valid_set)
  }


prepareData <- function(beta, lhb_buy) {
  #生成和日期，星期相关的特征
  lhb_buy <- lhb_buy %>%
    #有一天的数据有重复，这里过滤掉
    distinct(Date) %>%
    sort.data.frame(by = "Date") %>%
    mutate(WeekOfYear =  as.numeric(format(
      as.Date(Date, format = "%d-%m-%Y") + 6, "%U"
    ))) %>%
    mutate(MDay = mday(Date)) %>%
    mutate(Month = month(Date)) %>%
    mutate(Year = year(Date)) %>%
    mutate(DayOfWeek = ((wday(Date) + 5) %% 7 + 1)) %>%
    mutate(DayOfWeek1 = ifelse(DayOfWeek == 1, 1, 0)) %>%
    mutate(DayOfWeek2 = ifelse(DayOfWeek == 2, 1, 0)) %>%
    mutate(DayOfWeek3 = ifelse(DayOfWeek == 3, 1, 0)) %>%
    mutate(DayOfWeek4 = ifelse(DayOfWeek == 4, 1, 0)) %>%
    mutate(DayOfWeek5 = ifelse(DayOfWeek == 5, 1, 0)) %>%
    mutate(DayOfWeek6 = ifelse(DayOfWeek == 6, 1, 0)) %>%
    mutate(DayOfWeek7 = ifelse(DayOfWeek == 7, 1, 0)) %>%
    mutate(DateTrend = as.integer(difftime(Date, min(Date), units = 'days')) + 1) %>%
    mutate(DateTrendLog = log(as.integer(difftime(
      Date, min(Date), units = 'days'
    )) + 1))
  
  #2015-10-12到2015-11-13号这段时间的数据很大，人为做衰减(目前没有衰减)
  lhb_subset <-
    subset(lhb_buy, Date >= "2015-10-12" & Date <= "2015-11-13")
  lhb_subset$realSales <- lhb_subset$realSales * beta
  lhb_buy[which(lhb_buy$Date >= "2015-10-12" &
                  lhb_buy$Date <= "2015-11-13"), ] <- NA
  lhb_buy_new <- filter(lhb_buy, !is.na(Date)) %>%
    bind_rows(lhb_subset) %>%
    sort.data.frame(by = "Date") %>%
    mutate(Sales = log(realSales)) %>%
    mutate(First = Sales)
  
  #读入节假日的数据
  specialDays <-
    read.csv("../data/SpecialDays.csv", as.is = TRUE) %>%
    mutate(Date = as.Date(special_date)) %>%
    select(Date, holiday) %>%
    mutate(Year = year(Date)) %>%
    filter(Date > "2015-04-01" & holiday != 0)
  
  #用节假日的数据生成节假日前后一周的数据，用来对目标数据打标签
  holidayMinDate <-
    aggregate(Date ~ Year + holiday, specialDays, function(x)
      min(x))
  holidayMaxDate <-
    aggregate(Date ~ Year + holiday, specialDays, function(x)
      max(x))
  beforeHolidays <-
    generateNdaysTagNearHoliday(holidayMinDate$Date,
                                BeforeOrNot = TRUE,
                                days = c(1, 2, 3))
  afterHolidays <-
    generateNdaysTagNearHoliday(holidayMaxDate$Date,
                                BeforeOrNot = FALSE,
                                days = c(1, 2, 3))
  lhb_buy_new <- lhb_buy_new %>%
    mutate(BeforeHolidays = ifelse(Date %in% beforeHolidays, 1, 0)) %>%
    mutate(AfterHolidays = ifelse(Date %in% afterHolidays, 1, 0)) %>%
    mutate(IsHolidays = ifelse(Date %in% specialDays$Date, 1, 0))
  
  #将过去N周对应工作日的中位数组织在一起
  week_medians <- make_week_medians(lhb_buy_new, c(1, 3, 5, 7, 9))
  lhb_buy_new <-
    left_join(lhb_buy_new, week_medians, by = "Date", copy = TRUE)
  
  #过去N天的平均数组织在一起，这里数据的周期为5,所以选择5的倍数
  NDaysMean <- ndays_mean(lhb_buy_new, c(5, 10, 15, 20, 25, 30))
  lhb_buy_new <-
    left_join(lhb_buy_new, NDaysMean, by = "Date", copy = TRUE)
  
  #过去N周对应工作日的数据
  NWeekDay <-  makeNweekDay(lhb_buy_new, c(0, 1, 2, 3, 4, 5))
  lhb_buy_new <-
    left_join(lhb_buy_new, NWeekDay, by = "Date", copy = TRUE)
  
  lhb_buy_new
}

xparams <- list(
  objective = "reg:linear",
  booster = "gbtree",
  eta = 0.01,
  max_depth = 5,
  subsample = 0.5,
  colsample_bytree = 0.7,
  silent = 1
)

rmspe_basic <- function(predicted, actual) {
  if (length(predicted) != length(actual)) {
    stop("predicted and actual have different lengths")
  } else{
    sqrt(mean(((
      actual - predicted
    ) / actual) ^ 2))
  }
}

xgb_rmspe_for_model <- function(predicted, dtrain) {
  list(metric = "xgb_rmspe_for_model",
       value = rmspe_basic(exp(predicted), exp(getinfo(dtrain, 'label'))))
}

trainingmodelloop <-
  function(lhb_new,
           xgb_features,
           type,
           predict_interval = 7) {
    fold <-
      make_fold_range(lhb_new, validlength = 7, predictlength = 7)
    
    train_tr <-
      select(fold$train, matches("^Sales$"), one_of(c("Date", xgb_features)))
    test_tr <-
      select(fold$test, matches("^Sales$"), one_of(c("Date", xgb_features)))
    validate_tr <-
      select(fold$actual, matches("^Sales$"), one_of(c("Date", xgb_features)))
    
    fold_pred_tr <-
      predict_xgboost(
        train_tr,
        test_tr,
        xgb_rmspe_for_model,
        validate_tr,
        params = xparams,
        nrounds = 2001
      )
    
    # print("before")
    # names <- dimnames(train_tr %>% select(-Sales,-Date))[[2]]
    # importance_matrix <- xgb.importance(names, model = fold_pred_tr$fit)
    # xgb.plot.importance(importance_matrix)
    # print("after")
    pred <- fold_pred_tr$predicted %>%
      mutate(Sales = exp(Sales),
             PredictedSales = exp(PredictedSales))
    list(
      date = pred$Date,
      real = pred$Sales,
      guess = pred$PredictedSales
    )
  }

