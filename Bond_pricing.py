
import datetime
import math

def calc_dates(valu, matur): #function to find accrued dates and how many cash flows we will receive
    years = int((matur.year) - (valu.year)) #(A): This assumes maturity month and days are more than valuation month and date
    matur_day = (matur.day)
    matur_month = (matur.month)
    valu_day = (valu.day)
    valu_month = (valu.month)
    valu_year = (valu.year)
    next_cf = (datetime.date(valu_year,matur_month,matur_day))
    x = int((next_cf - valu).days)
    if (x < 0): # This is to compensate assumption (A)
        next_cf = (datetime.date((valu_year+1),matur_month,matur_day))
        years -= 1
    acc_days = int((next_cf - datetime.date(valu_year, valu_month, valu_day)).days) # trying to find how manys days left till next coupon is due
    if (acc_days != 0): # condition to check if there are accrued dates. Basically buying the bond between coupons
        years += 1
        acc_intr = calc_acc_interest(acc_days,coupon)
    else: # condition to check if bond is bought when on same day when coupon was stripped. No need to calculate accrued interest
            acc_intr = 0
    return (acc_days,acc_intr, years)


def calc_acc_interest(acc_days,coupon): #function to find accrued interest
    acc_intr = ((365-acc_days)/365)*coupon
    return acc_intr


def calc_termstruct (acc_days, frequency, discount_curve:dict): #function to get the actual interest termstructure while discounting
    if (acc_days !=0): #will make a custom T.S. based on our accrued dates
        acc = acc_days/365
        m = (list(discount_curve.values())[-1]-discount_curve[1])/(list(discount_curve)[-1]-1) #calculate slope
        c = discount_curve[1]-(m*1) # calculate intercept
        discount_curve2 = {}
        for i in range(0,frequency+1):
            key = i+acc
            if (key <= list(discount_curve)[0]): #this is incase the accrued days is less than 0.25 as in that case we do flat extrapolation
                discount_curve2[acc] = list(discount_curve.values())[0]
            elif (key > list(discount_curve)[0]):
                if (i < list(discount_curve)[-1]):
                    value = round(m*key+c,4)
                    discount_curve2[key] = value
                else:
                    discount_curve2[key] = list(discount_curve.values())[-1]
        ###print("Discount Curve: ",discount_curve2)
        return discount_curve2
    if (acc_days == 0): # incase we buy bond on coupon strp date. No custom T.S. required
        for i in list(discount_curve):
            if i < 1: #deleting T.S. lower than 1 year as its not required
                del discount_curve[i] 
        max_disc = list(discount_curve.values())[-1]
        if list(discount_curve)[-1] < frequency: #adding T.S. if frequency of c.f. is more than the max. T.S. limit
            for i in range((list(discount_curve)[-1])+1,frequency+1):
                discount_curve[i] = max_disc
        ###print("Discount Curve: ",discount_curve)
        return discount_curve


def calc_price(coupon, frequency, face_value, act_discount_curve:dict):
    pv = []
    discount_curve_time = list(act_discount_curve)
    discount_curve_rates = list(act_discount_curve.values())
    e= math.e
    #print(frequency)
    for i in range(frequency):
        if (i<frequency-1):
            pv.append(coupon*(e**(-1*(discount_curve_rates[i])*(discount_curve_time[i]))))
        else:
            pv.append((coupon+face_value)*(e**(-1*(discount_curve_rates[i])*(discount_curve_time[i]))))
    print("Cashflow: ",pv)
    pv_sum = sum(pv)
    return pv_sum


if __name__ == '__main__':
    #inputs
    face_value = 100
    coupon_rate= 0.05
    coupon = coupon_rate*face_value
    discount_curve = {0.25: 0.012,0.5:0.0118,1:0.0119,2:0.0175,3:0.0232,4:0.0282,5:0.0333}
    valu = datetime.date(2016,10,4)
    matur = datetime.date(2023,10,5)
    #end inputs

    #get accrued days and frequency of how many time we are going to receive the cashflow
    acc_days, acc_intr, frequency = calc_dates(valu,matur)
        
    #get the interest rate term structure
    act_discount_curve = calc_termstruct(acc_days,frequency,discount_curve)
        
    #finally calculate the price
    price = calc_price(coupon, frequency, face_value, act_discount_curve)
    print("Accrued days, no. of cfs: ",acc_days,frequency)
    print("Bond Price: ",round(price,4))