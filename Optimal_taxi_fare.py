#The student needs to get on a train that leaves from the station D kilometres away in T minutes.

#She can get a taxi that drives at V1 km/h for the price of R €/km or she can walk at V2 km/h for free.

#A correct solution will be a function that returns the minimum price she needs to pay the taxi driver or the string "Won't make it!".

#All the inputs will be positive integers, the output has to be a string containing a number with two decimal places - or "Won't make it!" if that is the case.

#It won't take her any time to get on the taxi or the train.

#In non-trivial cases you need to combine walking and riding the taxi so that she makes it, but pays as little as possible.

d =8
t = 10
v1 = 90
r = 2
v2 = 6


def calculate_optimal_fare(d, t, v1, r, v2):
    d = d * 1000
    t = t * 60
    v1 = v1 * 10 / 36
    r = r / 1000
    v2 = v2 * 10 / 36

    if t > d / v2:
        return "0.00"

    if t < d / v1:
        return "Won't make it!"

    time_walk = 0
    d_walk = 0

    d_taxi = d
    time_drive = d_taxi / v1
    print(str(round(time_drive, 2)) + "  time of Taxi drive")

    while time_walk + time_drive < t:
        diverence = 1.00
        d_walk += diverence
        d_taxi -= diverence
        time_walk = float((d_walk) / v2)
        time_walk = float("%.2f" % time_walk)
        time_drive = float((d_taxi) / v1)
        time_drive = float("%.2f" % time_drive)

    print(str(d_taxi) + " way of taxi")

    d_price = float(d_taxi * r)
    print(d_price)
    return str("%.2f" % d_price)


calculate_optimal_fare(d, t, v1, r, v2)