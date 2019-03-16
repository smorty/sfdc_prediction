if (getwd() != "C:/Users/MortensenS19/Documents/DSI/Capstone/Data/2019.02.25") {
  setwd("C:/Users/MortensenS19/Documents/DSI/Capstone/Data/2019.02.25")}
getwd()

library(readr)
library(tidyverse)
library(lubridate)
library(ROSE)
library(caret)
library(randomForest)

# Read in data===================================================================================================================

data_raw <- read.csv("Oppty_Acct_df.csv")

# Preprocessing==================================================================================================================

# Filter to only closed deals
data_closed = data_raw %>% filter(CLOSED__C==1)

# Select relevant variables
target = c("WON__C")
features = c("AMOUNT",
             "Code_1",
             "CREDIT_LIMIT_ESTABLISHED__C",
             "TYPE",
             "CORE_RECORD_TYPE__C",
             "ENTERPRISE_ACCOUNT__C_x",
             # "ANNUALREVENUE",
             "ACCOUNT_TIER__C",
             "ACCOUNT_TYPE__C",
             "CUSTOMER_CLASSIFICATION__C",
             "OPENTIME",
             "LASTACTTIME",
             "VALID_OPENTIME",
             "FIELDS_COMPLETED",
             "QUALIFICATION_APPROVAL_NA",
             "TASK_COUNT",
             "DIVISION__C")
all_variables = append(target,features)
data = data_closed %>% select(all_variables)

table(is.na(data$ANNUALREVENUE))
table(is.na(data$AMOUNT))
table(data$CREDIT_LIMIT_ESTABLISHED__C)

# Create test and train sets
set.seed(123)
train_idx = createDataPartition(data$WON__C, p = 0.5, list=FALSE)
train = data[train_idx,]
test = data[-train_idx,]

# Modeling=======================================================================================================================

# Establish win rate baseline
win_tbl = table(data$WON__C)
(win_pct = win_tbl[2]/sum(win_tbl))*100

# Logistic regression-----------------------------------------------------
train.glm = glm(WON__C ~ .,
                data = train, family=binomial(link = "logit"))

print(summary(train.glm))

# Prediction and accuracy
predict.glm = predict(train.glm, newdata = test, type='response')
# Confusion matrix
conf_mat.glm = table(test$WON__C, predict.glm > 0.55)
print(conf_mat.glm)
# Loss accuracy
print(conf_mat.glm[1,1]/sum(conf_mat.glm[1,]))
# Win accuracy
print(conf_mat.glm[2,2]/sum(conf_mat.glm[2,]))
# Overall accuracy
print((conf_mat.glm[2,2] + conf_mat.glm[1,1])/sum(conf_mat.glm))

# Percentage of test data being predicted on
sum(conf_mat.glm)/nrow(test)

# Random forest------------------------------------------------------------
start.time = Sys.time()
train.rf = randomForest(WON__C ~ .,
                        data = train, na.action=na.exclude, importance=T)
print(Sys.time() - start.time)

# Importance plot
varImpPlot(train.rf, type=1, color="black", lcolor="black")

# Prediction and accuracy
predict.rf = predict(train.rf, test, predict.all=TRUE)$aggregate
# Confusion matrix
conf_mat.rf = table(test$WON__C, predict.rf > 0.55)
print(conf_mat.rf)
# Loss accuracy
print(conf_mat.rf[1,1]/sum(conf_mat.rf[1,]))
# Win accuracy
print(conf_mat.rf[2,2]/sum(conf_mat.rf[2,]))
# Overall accuracy
print((conf_mat.rf[2,2] + conf_mat.rf[1,1])/sum(conf_mat.rf))

# Percentage of test data being predicted on
sum(conf_mat.rf)/nrow(test)
