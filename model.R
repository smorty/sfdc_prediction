if (getwd() != "C:/Users/MortensenS19/Documents/DSI/Capstone/Data/2019.02.25") {
  setwd("C:/Users/MortensenS19/Documents/DSI/Capstone/Data/2019.02.25")}
getwd()

library(readr)
library(tidyverse)
library(lubridate)

# Read in data===================================================================================================================

opportunity_raw <- read.csv("Oppty_Acct_df.csv")


# Extract variables (probably not needed)========================================================================================
y <- opportunity$WON__C #y variable
probability <- opportunity$PROBABILITY #probability produces high R-squared

#for NLP
description <- opportunity$DESCRIPTION
crit_biz_issue <- opportunity$CRITICAL_BUSINESS_ISSUES__C #high %null
cust_hot_button <- opportunity$CUSTOMER_HOT_BUTTONS__C #high %null
cust_pressure_desc <- opportunity$CUSTOMER_PRESSURES_DESCRIPTION__C #high %null
fold_cart_cust <- opportunity$FOLDING_CARTON_CUSTOMER__C #high %null

#categorical
lead_source <- opportunity$LEADSOURCE
currency <- opportunity$CURRENCYISOCODE
region <- opportunity$REGION__C
area <- opportunity$AREA__C
division <- opportunity$DIVISION__C
opp_division <- opportunity$OPPORTUNITY_DIVISION__C #figure out what this is relative to division
owner <- opportunity$OPPORTUNITY_OWNER_MANAGER_EMAIL_FORMULA__C #280 total
NAICS_code <- opportunity$NAICS_CODE__C #use a wildcard on this: farming, manufacturing, wholesale
industry <- opportunity$INDUSTRY__C #needs cleaning
paprbrd_sub_util <- opportunity$PAPERBOARD_SUBSTRATES_UTILIZED__C #needs cleaning
ship_to_state <- opportunity$SHIP_TO_STATE__C #needs cleaning

#account fields
account_tier <- opportunity$ACCOUNT_TIER__C
account_type <- opportunity$ACCOUNT_TYPE__C
customer_class <- opportunity$CUSTOMER_CLASSIFICATION__C
enterp_acc <- opportunity$ENTERPRISE_ACCOUNT__C_x

#datetime
created_date <- opportunity$CREATEDDATE
close_date <- opportunity$CLOSEDATE
last_activity_date <- opportunity$LASTACTIVITYDATE
fiscal_quarter <- opportunity$FISCALQUARTER
fiscal_year <- opportunity$FISCALYEAR
stage_change_date <- opportunity$STAGE_CHANGE_DATE_STAMP__C

# Pre-process data==============================================================================================================

#filter to only closed deals
opportunity1 = opportunity_raw %>% filter(CLOSED__C==1)

#filter to only relevant dates
opportunity1$CREATEDDATE = as_date(opportunity1$CREATEDDATE)
date_filter = ymd("2016-04-01")
opportunity = opportunity1 %>% filter(CREATEDDATE >= date_filter)

#drop unnecessary variables
drops <- c("STAGENAME", "PROBABILITY","DESCRIPTION","NEXTSTEP","CURRENCYISOCODE", "CRITICAL_BUSINESS_ISSUES__C", "CUSTOMER_HOT_BUTTONS__C", "CUSTOMER_PRESSURES_DESCRIPTION__C", "OPPORTUNITY_OWNER_MANAGER_EMAIL_FORMULA__C", "INDUSTRY__C", "PAPERBOARD_SUBSTRATES_UTILIZED__C", "REGION__C", "AREA__C", "DIVISION__C", "OPPORTUNITY_DIVISION__C", "SHIP_TO_STATE__C", "CLOSED__C", "CREATEDDATE", "CLOSEDATE", "LASTACTIVITYDATE", "STAGE_CHANGE_DATE_STAMP__C")
opportunity <- opportunity[ , !(names(opportunity) %in% drops)]

#group LeadSource values
opportunity$LEADSOURCE[opportunity$LEADSOURCE=="APS Mandrel-Formed Campaign"] <- "Other"
opportunity$LEADSOURCECLEAN <- opportunity$LEADSOURCE
ls_table <- as.data.frame(table(lead_source))
ls_table$reorg <- ifelse(ls_table$Freq <= 15,"Other", "Drop")
ls_table2 <- ls_table[ls_table$reorg=="Other", ]
ls_table2$lead_source
opportunity$LEADSOURCECLEAN[opportunity$LEADSOURCECLEAN%in%ls_table2$lead_source] <- "Other"

#filter to only relevant dates


# Modeling=======================================================================================================================

# install.packages("ROSE")
library(ROSE)
# install.packages("caret")
library(caret)
# install.packages("randomForest")
library(randomForest)

# -----------------------------------------------------------------------
opportunity.lm <- lm(WON__C ~ AMOUNT + factor(Code_1) + factor(Code_2) + factor(Code_industry) + factor(CREDIT_LIMIT_ESTABLISHED__C) + factor(LEADSOURCECLEAN) + factor(TYPE) + factor(BIG_DEAL_APPROVAL__C) + factor(CORE_RECORD_TYPE__C) + factor(MATERIAL_SAMPLES_APPROVAL_STATUS__C) + factor(QUALIFICATION_APPROVAL_STATUS__C) + factor(ENTERPRISE_ACCOUNT__C_x) + factor(CORE_RECORD_TYPE__C), data = opportunity)
summary(opportunity.lm)
#highest RSQ so far: .221

opportunity.lm <- lm(WON__C ~ ANNUALREVENUE + factor(Code_1) + factor(Code_2) + factor(Code_industry) + factor(ACCOUNT_TIER__C) + factor(ACCOUNT_TYPE__C) + factor(CUSTOMER_CLASSIFICATION__C) + AMOUNT + factor(CREDIT_LIMIT_ESTABLISHED__C) + factor(LEADSOURCECLEAN) + factor(TYPE) + factor(BIG_DEAL_APPROVAL__C) + factor(CORE_RECORD_TYPE__C) + factor(MATERIAL_SAMPLES_APPROVAL_STATUS__C) + factor(QUALIFICATION_APPROVAL_STATUS__C) + factor(ENTERPRISE_ACCOUNT__C_x) + factor(CORE_RECORD_TYPE__C), data = opportunity)
summary(opportunity.lm)
#highest RSQ so far: .3499
#with variables from "account" table, the adjusted R square decreased

# ------------------------------------------------------------------------

set.seed(201)
intrain_m <- createDataPartition(opportunity$WON__C, p = 0.5, list = FALSE)

# construct train and test dataset
train_m1 <- opportunity[intrain_m, ] # train_m1: train, monthly, train set 1
validation_m1 <- opportunity[-intrain_m, ] # validation_m1: validation, monthly, validation set 1

table(train_m1$LEADSOURCECLEAN)
table(validation_m1$LEADSOURCECLEAN)

opportunity.glm <- glm(WON__C ~ AMOUNT + factor(Code_1) + factor(Code_2) + factor(Code_industry) + factor(ACCOUNT_TIER__C) + factor(ACCOUNT_TYPE__C) + factor(CUSTOMER_CLASSIFICATION__C) + factor(LEADSOURCECLEAN) + factor(CREDIT_LIMIT_ESTABLISHED__C) + factor(BIG_DEAL_APPROVAL__C) + factor(CORE_RECORD_TYPE__C) + factor(MATERIAL_SAMPLES_APPROVAL_STATUS__C) + factor(QUALIFICATION_APPROVAL_STATUS__C) + factor(ENTERPRISE_ACCOUNT__C_x) + factor(CORE_RECORD_TYPE__C)
                       , data = train_m1, family=binomial(link = "logit"))
summary(opportunity.glm)
# AIC: 43628

predictvalid <- predict(opportunity.glm, newdata = validation_m1, type = 'response')
conf_mat <- table(validation_m1$WON__C, predictvalid > 0.55)
conf_mat

conf_mat[1,1]/(sum(conf_mat[1,])) #0.7461687 - 1/23/2019 0.8428346 - 2/27/2019 0.7192964
conf_mat[2,2]/(sum(conf_mat[2,])) #0.646136 - 1/23/2019 0.6439109 - 2/27/2019 0.670183

predlog <- predict(opportunity.glm, newdata = opportunity)
roc.curve(opportunity$WON__C, predlog) #error "Error in if (auc < 0.5) { : missing value where TRUE/FALSE needed", need to check with Karen

# ------------------------------------------------------------------------
# Random Forest

train_m2 <- train_m1
glimpse(train_m2)
train_m2$WON__C <- as.factor(train_m2$WON__C)
train_m2 <- as.data.frame(train_m2)

names(train_m2)

rf <- randomForest(WON__C ~ LEADSOURCECLEAN + Code_1 + Code_2 + Code_industry + ACCOUNT_TIER__C + ACCOUNT_TYPE__C + CUSTOMER_CLASSIFICATION__C + CREDIT_LIMIT_ESTABLISHED__C + BIG_DEAL_APPROVAL__C + CORE_RECORD_TYPE__C + MATERIAL_SAMPLES_APPROVAL_STATUS__C + QUALIFICATION_APPROVAL_STATUS__C + ENTERPRISE_ACCOUNT__C_x + CORE_RECORD_TYPE__C
                   , data = train_m2, na.action=na.exclude, importance=T)
print(rf)
varImpPlot(rf, type=1)
View(importance(rf, type=1))
rf
