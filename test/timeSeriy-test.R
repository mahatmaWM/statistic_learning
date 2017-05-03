# rmse = function(pred,test)
# { 
#     res<- sqrt(mean((pred-test)^2) )
#     res
# }


#导入数据
passenger = read.csv('D:\\passenger.csv', header = F)

#把数据变成time series, frequency=12表示以月份为单位
pt <- ts(passenger, frequency = 12, start = c(1949, 1)) #
ts.plot(pt)

#得到训练与测试数据
train <- window(pt, start = c(1949, 1), end = c(1959, 12))
test <- window(pt, start = c(1960, 1), end = c(1960, 12))
ts.plot(train)
ts.plot(test)
#导入需要的包
library(forecast)

#方法一，未来值是历史值的平均
pred_meanf <- meanf(train, h = 12)
accuracy(test, pred_meanf$mean) #226.2657
plot(pred_meanf)

#方法二，指数衰减 相当于 ARIMA(0,1,0) random walk
#当去平均值得时候，每个历史点的权值可以不一样。
#最自然的就是越近的点赋予越大的权重。
pred_naive <- naive(train, h = 12)
accuracy(pred_naive$mean, test) #102.9765
plot(pred_naive)

#知道周期的指数衰减
#假设已知数据的周期，那么就用前一个周期对应的时刻作为下一个周期对应时刻的预测值
pred_snaive <- snaive(train, h = 12)
accuracy(pred_snaive$mean, test)#50.70832
plot(pred_snaive)

#方法三，for a random walk with drift model applied to x
#即用最后一个点的值加上数据的平均趋势
pred_rwf <- rwf(train, h = 12, drift = T)
accuracy(pred_rwf$mean, test)#92.66636
plot(pred_rwf)

#方法四,Holt-Winters
#三阶指数平滑 
#Holt-Winters的思想是把数据分解成三个成分：
#平均水平（level），趋势（trend），周期性（seasonality）
fit <- ets(train)
accuracy(predict(fit, 12), test) #24.390252
par(mfrow = c(1, 2))
ts.plot(pt)
plot(forecast(fit,12))


#方法五，ARIMA
#寻找原始数据变成稳定序列所需要的diff次数
frequency(train)
ndiffs(train)
nsdiffs(train)

#观察图形，对数据进行diff操作，寻找pq值
tsdisplay(train)
tsdisplay(diff(train)) #pq都有值，有周期性，从图上看在4阶左右
tsdisplay(diff(train, lag = 12))

#自动搜寻
fit <-
  auto.arima(
    train,
    stepwise = FALSE,
    approximation = FALSE,
    parallel = TRUE,
    trace = FALSE,
    max.P = 3,
    max.Q = 3,
    start.P = 0,
    start.Q = 0,
    test=c("kpss","adf","pp"), 
    seasonal.test=c("ocsb","ch"),
    ic = c("aicc", "aic", "bic")
  )
summary(fit)
#ARIMA(0,1,3)(0,1,0)[12]

#测试自动找出的参数
ma = arima(train,
           order = c(0, 1, 3),
           seasonal = list(order = c(0, 1, 0), period = 12))
p <- predict(ma, 12)
plot(forecast(ma, 12))
accuracy(p$pred, test)  #22.96189
tsdisplay(ma$residuals)
Box.test(ma$residuals,
         lag = 12,
         type = "Box-Pierce",
         fitdf = 3)


#再调整参数
ma = arima(train,
           order = c(0, 1, 3),
           seasonal = list(order = c(0, 1, 3), period = 12))
#summary(ma)
p <- predict(ma, 12)
plot(forecast(ma, 12))
accuracy(p$pred, test)  #18.55567
tsdisplay(ma$residuals)
Box.test(ma$residuals,
         lag = 12,
         type = "Box-Pierce",
         fitdf = 3)

par(mfrow = c(1, 2))
ts.plot(pt)
plot(forecast(ma,12))

#===========================
#xreg参数引入其它维度因子的例子

x <- c(1774, 1706, 1288, 1276, 2350, 1821, 1712, 1654, 1680, 1451, 
 1275, 2140, 1747, 1749, 1770, 1797, 1485, 1299, 2330, 1822, 1627, 
 1847, 1797, 1452, 1328, 2363, 1998, 1864, 2088, 2084, 594, 884, 
 1968, 1858, 1640, 1823, 1938, 1490, 1312, 2312, 1937, 1617, 1643, 
 1468, 1381, 1276, 2228, 1756, 1465, 1716, 1601, 1340, 1192, 2231, 
 1768, 1623, 1444, 1575, 1375, 1267, 2475, 1630, 1505, 1810, 1601, 
 1123, 1324, 2245, 1844, 1613, 1710, 1546, 1290, 1366, 2427, 1783, 
 1588, 1505, 1398, 1226, 1321, 2299, 1047, 1735, 1633, 1508, 1323, 
 1317, 2323, 1826, 1615, 1750, 1572, 1273, 1365, 2373, 2074, 1809, 
 1889, 1521, 1314, 1512, 2462, 1836, 1750, 1808, 1585, 1387, 1428, 
 2176, 1732, 1752, 1665, 1425, 1028, 1194, 2159, 1840, 1684, 1711, 
 1653, 1360, 1422, 2328, 1798, 1723, 1827, 1499, 1289, 1476, 2219, 
 1824, 1606, 1627, 1459, 1324, 1354, 2150, 1728, 1743, 1697, 1511, 
 1285, 1426, 2076, 1792, 1519, 1478, 1191, 1122, 1241, 2105, 1818, 
 1599, 1663, 1319, 1219, 1452, 2091, 1771, 1710, 2000, 1518, 1479, 
 1586, 1848, 2113, 1648, 1542, 1220, 1299, 1452, 2290, 1944, 1701, 
 1709, 1462, 1312, 1365, 2326, 1971, 1709, 1700, 1687, 1493, 1523, 
 2382, 1938, 1658, 1713, 1525, 1413, 1363, 2349, 1923, 1726, 1862, 
 1686, 1534, 1280, 2233, 1733, 1520, 1537, 1569, 1367, 1129, 2024, 
 1645, 1510, 1469, 1533, 1281, 1212, 2099, 1769, 1684, 1842, 1654, 
 1369, 1353, 2415, 1948, 1841, 1928, 1790, 1547, 1465, 2260, 1895, 
 1700, 1838, 1614, 1528, 1268, 2192, 1705, 1494, 1697, 1588, 1324, 
 1193, 2049, 1672, 1801, 1487, 1319, 1289, 1302, 2316, 1945, 1771, 
 2027, 2053, 1639, 1372, 2198, 1692, 1546, 1809, 1787, 1360, 1182, 
 2157, 1690, 1494, 1731, 1633, 1299, 1291, 2164, 1667, 1535, 1822, 
 1813, 1510, 1396, 2308, 2110, 2128, 2316, 2249, 1789, 1886, 2463, 
 2257, 2212, 2608, 2284, 2034, 1996, 2686, 2459, 2340, 2383, 2507, 
 2304, 2740, 1869, 654, 1068, 1720, 1904, 1666, 1877, 2100, 504, 
 1482, 1686, 1707, 1306, 1417, 2135, 1787, 1675, 1934, 1931, 1456)

y=auto.arima(x)
summary(y)
#plot(forecast(y,h=30))
#points(1:length(x),fitted(y),type="l",col="green")

holiday <- 
c(FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, 
TRUE, FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 
FALSE, FALSE, FALSE)

y<-auto.arima(x, xreg=holiday)
summary(y)
#plot(forecast(y,xreg=data.frame(holiday=rep(FALSE,30))))
#points(1:length(x),fitted(y),type="l",col="green")
