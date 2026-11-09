from abc import ABC,abstractmethod
from room_inventory import room_types
from datetime import date,datetime,timedelta
from database import get_returning_guest

class Guest:
    def __init__(self, name, mobile_number, email_id):
        self.name = name
        self.mobile_number = mobile_number
        self.email_id = email_id

class Booking:

    def __init__(self,guest,room_type,number_of_guest,booking_date,checkin,checkout,room_no,status,total_pay):
        self.guest=guest
        self.room_type=room_type
        self.number_of_guest=number_of_guest
        self.booking_date=booking_date
        self.checkin=checkin
        self.checkout=checkout
        self.room_no=room_no
        self.status=status
        self.total_pay=total_pay

#creating classes
class Room(ABC):
    def __init__(self,room_type,number_of_guest,checkin,checkout,mobile_number):
        self.room_type=room_type
        self.number_of_guest=number_of_guest
        self.checkin=checkin
        self.checkout=checkout
        self.mobile_number=mobile_number
    @abstractmethod   
    def normal_room_charges(self):
        pass
    @abstractmethod
    def extra_guest_charge(self):
        pass
    @abstractmethod
    def weekends_charges(self):
        pass
    @abstractmethod
    def breakfast(self):
        pass
    @abstractmethod
    def discount_on_room_charges(self):
        pass
    @abstractmethod
    def loyality_discount(self):
        pass
    @abstractmethod
    def gst(self):
        pass
    


class StandardRoom(Room):
    def __init__(self, room_type, number_of_guest, checkin, checkout, mobile_number):
        super().__init__(room_type, number_of_guest, checkin, checkout, mobile_number)
        self.breakfast_details = None
        
    def normal_room_charges(self):

        days = []
        total_base_price = 0

        for i in room_types:
            if i['room_type'].lower() == self.room_type.lower():
                base_price = i['base_rate']
                break

        current_date = self.checkin

        while current_date < self.checkout:
            days.append(current_date.weekday())
            current_date += timedelta(days=1)

        for i in range(len(days)):
            total_base_price = total_base_price + base_price

        return total_base_price, base_price
    
    def weekends_charges(self):
        days=[]
        count_fri_sat=0
        total_base_price,base_price=self.normal_room_charges()
        weekend_charge=0
        current_date=self.checkin

        while current_date<self.checkout:
            days.append(current_date.weekday())
            current_date+=timedelta(days=1)

        for i in days:
            if i==4 or i==5:
                count_fri_sat=count_fri_sat+1

        for i in range(count_fri_sat):
            weekend_charge=weekend_charge+base_price*0.20

        normal_weekend_charge=base_price*0.20

        return weekend_charge,normal_weekend_charge
    
    def breakfast(self):
        if self.breakfast_details is not None:
            return self.breakfast_details
        total_break_fast_charge=0
        normal_break_fast_charge=0

        while True:
            break_fast=input("Do you want breakfast for all days? yes or no: ").strip().lower()
            if break_fast=="yes":
                break
            elif break_fast=="no":
                break
            else:
                print("please enter yes or no")

        if break_fast=="yes":
            for i in room_types:
                if self.room_type.lower()==i['room_type'].lower():
                    charge=i['breakfast_charge']
                    normal_break_fast_charge=self.number_of_guest*charge
                    break

            days=(self.checkout-self.checkin).days
            total_break_fast_charge=normal_break_fast_charge*days

        self.breakfast_details = (total_break_fast_charge, normal_break_fast_charge)
        return self.breakfast_details

    def discount_on_room_charges(self):
        total_base_price,base_price=self.normal_room_charges()
        total_weekend_charge,normal_weekend_charge=self.weekends_charges()

        days=[]
        discount=0
        normal_discount=0
        current_date=self.checkin

        while current_date<self.checkout:
            days.append(current_date.weekday())
            current_date+=timedelta(days=1)

        if len(days)>=7:
            discount=(total_base_price+total_weekend_charge)*0.1
            normal_discount=(base_price+normal_weekend_charge)*0.1

        return discount,normal_discount

    def loyality_discount(self):
        returning_guest=get_returning_guest(self.mobile_number)
        loyality_discount=0
        normal_loyality_discount=0
        total_weekend_charge,normal_weekend_charge=self.weekends_charges()
        total_base_price,base_price=self.normal_room_charges()
        discount,normal_discount=self.discount_on_room_charges()

        amount_after_discount=total_base_price+total_weekend_charge-discount

        if len(returning_guest)>=3:
            loyality_discount=amount_after_discount*0.05
            normal_loyality_discount=(base_price+normal_weekend_charge-normal_discount)*0.05

        return loyality_discount,normal_loyality_discount
    def extra_guest_charge(self):
        extra_guest_charge=0
        return extra_guest_charge
        
    def gst(self):
        total_gst=0
        current_date=self.checkin

        total_base_price,base_price=self.normal_room_charges()
        total_weekend_charge,normal_weekend_charge=self.weekends_charges()
        total_break_fast_charge,normal_break_fast_charge=self.breakfast()
        total_discount,normal_discount=self.discount_on_room_charges()
        total_loyality_discount,normal_loyality_discount=self.loyality_discount()
        extra_guest_charge=self.extra_guest_charge()

        while current_date<self.checkout:
            weekend_charge=0

            if current_date.weekday()==4 or current_date.weekday()==5:
                weekend_charge=normal_weekend_charge

            room_tariff=base_price+weekend_charge

            daily_discount=0
            daily_loyality_discount=0

            if total_discount>0:
                daily_discount=room_tariff*0.1

            if total_loyality_discount>0:
                daily_loyality_discount=(room_tariff-daily_discount)*0.05

            taxable_amount=room_tariff+extra_guest_charge+normal_break_fast_charge-daily_discount-daily_loyality_discount

            if room_tariff<=7500:
                gst=taxable_amount*0.12
            else:
                gst=taxable_amount*0.18

            total_gst=total_gst+gst
            current_date+=timedelta(days=1)

        return total_gst

class DeluxeRoom(Room):
    def __init__(self,room_type,number_of_guest,checkin,checkout,mobile_number):
        super().__init__(room_type,number_of_guest,checkin,checkout,mobile_number)
        
    def normal_room_charges(self):

        days = []
        total_base_price = 0

        for i in room_types:
            if i['room_type'].lower() == self.room_type.lower():
                base_price = i['base_rate']
                break

        current_date = self.checkin

        while current_date < self.checkout:
            days.append(current_date.weekday())
            current_date += timedelta(days=1)

        for i in range(len(days)):
            total_base_price = total_base_price + base_price

        return total_base_price, base_price
    
    def weekends_charges(self):
        days=[]
        count_fri_sat=0
        total_base_price,base_price=self.normal_room_charges()
        weekend_charge=0
        current_date=self.checkin

        while current_date<self.checkout:
            days.append(current_date.weekday())
            current_date+=timedelta(days=1)

        for i in days:
            if i==4 or i==5:
                count_fri_sat=count_fri_sat+1

        for i in range(count_fri_sat):
            weekend_charge=weekend_charge+base_price*0.20

        normal_weekend_charge=base_price*0.20

        return weekend_charge,normal_weekend_charge
    def breakfast(self):
        total_break_fast_charge=0
        normal_break_fast_charge=0
        return total_break_fast_charge,normal_break_fast_charge
    def discount_on_room_charges(self):
        total_base_price,base_price=self.normal_room_charges()
        total_weekend_charge,normal_weekend_charge=self.weekends_charges()

        days=[]
        discount=0
        normal_discount=0
        current_date=self.checkin

        while current_date<self.checkout:
            days.append(current_date.weekday())
            current_date+=timedelta(days=1)

        if len(days)>=7:
            discount=(total_base_price+total_weekend_charge)*0.1
            normal_discount=(base_price+normal_weekend_charge)*0.1

        return discount,normal_discount

    def loyality_discount(self):
        returning_guest=get_returning_guest(self.mobile_number)
        loyality_discount=0
        normal_loyality_discount=0
        total_weekend_charge,normal_weekend_charge=self.weekends_charges()
        total_base_price,base_price=self.normal_room_charges()
        discount,normal_discount=self.discount_on_room_charges()

        amount_after_discount=total_base_price+total_weekend_charge-discount

        if len(returning_guest)>=3:
            loyality_discount=amount_after_discount*0.05
            normal_loyality_discount=(base_price+normal_weekend_charge-normal_discount)*0.05

        return loyality_discount,normal_loyality_discount
    def extra_guest_charge(self):
        extra_guest_charge=0
        per_day_extra_guest_charge=0
        guest_count=self.number_of_guest-2

        if self.number_of_guest>2:
            for i in range(guest_count):
                per_day_extra_guest_charge=per_day_extra_guest_charge+800

            days=(self.checkout-self.checkin).days
            extra_guest_charge=per_day_extra_guest_charge*days

        return extra_guest_charge,per_day_extra_guest_charge


        
    def gst(self):
        total_gst=0
        current_date=self.checkin

        total_base_price,base_price=self.normal_room_charges()
        total_weekend_charge,normal_weekend_charge=self.weekends_charges()
        total_break_fast_charge,normal_break_fast_charge=self.breakfast()
        total_discount,normal_discount=self.discount_on_room_charges()
        total_loyality_discount,normal_loyality_discount=self.loyality_discount()
        total_extra_guest_charge,per_day_extra_guest_charge=self.extra_guest_charge()

        while current_date<self.checkout:
            weekend_charge=0

            if current_date.weekday()==4 or current_date.weekday()==5:
                weekend_charge=normal_weekend_charge

            room_tariff=base_price+weekend_charge

            daily_discount=0
            daily_loyality_discount=0

            if total_discount>0:
                daily_discount=room_tariff*0.1

            if total_loyality_discount>0:
                daily_loyality_discount=(room_tariff-daily_discount)*0.05

            taxable_amount=room_tariff+per_day_extra_guest_charge+normal_break_fast_charge-daily_discount-daily_loyality_discount

            if room_tariff<=7500:
                gst=taxable_amount*0.12
            else:
                gst=taxable_amount*0.18

            total_gst=total_gst+gst
            current_date+=timedelta(days=1)

        return total_gst
        




class SuiteRoom(Room):
    def __init__(self,room_type,number_of_guest,checkin,checkout,mobile_number):
            super().__init__(room_type,number_of_guest,checkin,checkout,mobile_number)
            
    def normal_room_charges(self):

        days = []
        total_base_price = 0

        for i in room_types:
            if i['room_type'].lower() == self.room_type.lower():
                base_price = i['base_rate']
                break

        current_date = self.checkin

        while current_date < self.checkout:
            days.append(current_date.weekday())
            current_date += timedelta(days=1)

        for i in range(len(days)):
            total_base_price = total_base_price + base_price

        return total_base_price, base_price
    
    def weekends_charges(self):
        days=[]
        count_fri_sat=0
        total_base_price,base_price=self.normal_room_charges()
        weekend_charge=0
        current_date=self.checkin

        while current_date<self.checkout:
            days.append(current_date.weekday())
            current_date+=timedelta(days=1)

        for i in days:
            if i==4 or i==5:
                count_fri_sat=count_fri_sat+1

        for i in range(count_fri_sat):
            weekend_charge=weekend_charge+base_price*0.20

        normal_weekend_charge=base_price*0.20

        return weekend_charge,normal_weekend_charge
    def breakfast(self):
        total_break_fast_charge=0
        normal_break_fast_charge=0
        return total_break_fast_charge,normal_break_fast_charge
    def discount_on_room_charges(self):
        total_base_price,base_price=self.normal_room_charges()
        total_weekend_charge,normal_weekend_charge=self.weekends_charges()

        days=[]
        discount=0
        normal_discount=0
        current_date=self.checkin

        while current_date<self.checkout:
            days.append(current_date.weekday())
            current_date+=timedelta(days=1)

        if len(days)>=7:
            discount=(total_base_price+total_weekend_charge)*0.1
            normal_discount=(base_price+normal_weekend_charge)*0.1

        return discount,normal_discount

    def loyality_discount(self):
        returning_guest=get_returning_guest(self.mobile_number)
        loyality_discount=0
        normal_loyality_discount=0
        total_weekend_charge,normal_weekend_charge=self.weekends_charges()
        total_base_price,base_price=self.normal_room_charges()
        discount,normal_discount=self.discount_on_room_charges()

        amount_after_discount=total_base_price+total_weekend_charge-discount

        if len(returning_guest)>=3:
            loyality_discount=amount_after_discount*0.05
            normal_loyality_discount=(base_price+normal_weekend_charge-normal_discount)*0.05

        return loyality_discount,normal_loyality_discount
    def extra_guest_charge(self):
        extra_guest_charge=0
        per_day_extra_guest_charge=0
        guest_count=self.number_of_guest-2

        if self.number_of_guest>2:
            for i in range(guest_count):
                per_day_extra_guest_charge=per_day_extra_guest_charge+800

            days=(self.checkout-self.checkin).days
            extra_guest_charge=per_day_extra_guest_charge*days

        return extra_guest_charge,per_day_extra_guest_charge


        
    def gst(self):
        total_gst=0
        current_date=self.checkin

        total_base_price,base_price=self.normal_room_charges()
        total_weekend_charge,normal_weekend_charge=self.weekends_charges()
        total_break_fast_charge,normal_break_fast_charge=self.breakfast()
        total_discount,normal_discount=self.discount_on_room_charges()
        total_loyality_discount,normal_loyality_discount=self.loyality_discount()
        total_extra_guest_charge,per_day_extra_guest_charge=self.extra_guest_charge()

        while current_date<self.checkout:
            weekend_charge=0

            if current_date.weekday()==4 or current_date.weekday()==5:
                weekend_charge=normal_weekend_charge

            room_tariff=base_price+weekend_charge

            daily_discount=0
            daily_loyality_discount=0

            if total_discount>0:
                daily_discount=room_tariff*0.1

            if total_loyality_discount>0:
                daily_loyality_discount=(room_tariff-daily_discount)*0.05

            taxable_amount=room_tariff+per_day_extra_guest_charge+normal_break_fast_charge-daily_discount-daily_loyality_discount

            if room_tariff<=7500:
                gst=taxable_amount*0.12
            else:
                gst=taxable_amount*0.18

            total_gst=total_gst+gst
            current_date+=timedelta(days=1)

        return total_gst
        

