create database ola;
use ola;

#1- Retrieve all successful bookings:
create view succesfull_booking as
select * from rides1
where booking_status = 'success';
#2- Find the average ride distance for each vehicle type:
create view avg_ride_distance_for_each_vehicle_types as
select vehicle_type,AVG(ride_distance) 
as avg_distance from rides1
 group by vehicle_type; 
#3- Get the total number of cancelled rides by customers:
create view rides_cancelled_by_customer as
select count(*) from rides1
where booking_status='Canceled by customer';
select * from rides_cancelled_by_customer;
#4- List the top 5 customers who booked the highest number of rides:
create view top_5_customers as 
select customer_id,count(booking_id) as total_rides
from rides1 group by customer_id
order by total_rides desc limit 5;
select * from top_5_customers;
#5- Get the number of rides cancelled by customers due to  personal and car-related issues::
Create View Rides_cancelled_by_Drivers_P_C_Issues As
SELECT COUNT(*) FROM rides1
WHERE canceled_Rides_by_Driver = 'Personal & Car related issue';
select * from Rides_cancelled_by_Drivers_P_C_Issues;
#6-Find the maximum and minimum driver ratings for Prime Sedan bookings:
create view min_max_Drating as
SELECT 
    MIN(driver_ratings) AS min_rating, 
    MAX(driver_ratings) AS max_rating 
FROM rides1
WHERE vehicle_type = 'Prime sedan' AND driver_ratings IS NOT NULL AND driver_ratings != '';
select * from min_max_Drating;
#7- Retrieve all rides where payment was made using UPI:
create view upi_payments as 
select * from rides1
where payment_method='upi';
#8- Find the average customer rating per vehicle type:
Create View AVG_Cust_Rating As
SELECT Vehicle_Type, AVG(Customer_Rating) as avg_customer_rating
FROM rides1
GROUP BY Vehicle_Type;
select * from AVG_Cust_Rating;

#9- Calculate the total booking value of rides completed successfully:
Create View total_successful_ride_value As
SELECT SUM(Booking_Value) as total_successful_ride_value
FROM rides1
WHERE Booking_Status = 'Success';
select * from total_successful_ride_value;
#10- List all incomplete rides along with the reason
Create View Incomplete_Rides_Reason As
SELECT Booking_ID, Incomplete_Rides_Reason
FROM rides1
WHERE Incomplete_Rides = 'Yes';


#1- Retrieve all successful bookings:
select * from succesfull_booking;
#2- Find the average ride distance for each vehicle type:
select * from  avg_ride_distance_for_each_vehicle_types;
#3- Get the total number of cancelled rides by customers:
select * from rides_cancelled_by_customer;
#4- List the top 5 customers who booked the highest number of rides:
select * from top_5_customers;
#5- Get the number of rides cancelled by customers due to AC is not working and Driver asked to cancel:
Select * from Rides_cancelled_by_Drivers_P_C_Issues;
#6-Find the maximum and minimum driver ratings for Prime Sedan bookings:
Select * from Max_Min_Driver_Rating;
#7- Retrieve all rides where payment was made using UPI:
select * from upi_payments;
#8- Find the average customer rating per vehicle type:
Select * from AVG_Cust_Rating;
#9- Calculate the total booking value of rides completed successfully:
Select * from total_successful_ride_value;
#10- List all incomplete rides along with the reason
Select * from Incomplete_Rides_Reason;