
# Python program to find solutions to number difference triange puzzle at https://nrich.maths.org/927

debug = False

def check_vals (a,b,c,d):
    count = [0,0,0,0,0,0,0,0,0,0,0]

    # row 4 (check the inputs)
    # position 1
    if debug:
        print ("Position 1: " + str(a) + ", " + ''.join(str(e) for e in count))
    if (a < 1 or a > 10):
        return False
    # no need to check for prior value of 'a'
    count [a] = 1

    # position 2
    if debug:
        print ("Position 2: " + str(b) + ", " + ''.join(str(e) for e in count))
    if (b < 1 or b > 10):
        return False
    if count [b] == 1:
        return False
    count [b] = 1

    # position 3
    if debug:
        print ("Position 3: " + str(c) + ", " + ''.join(str(e) for e in count))
    if (c < 1 or c > 10):
        return False
    if count [c] == 1:
        return False
    count [c] = 1

    # position 4
    if debug:
        print ("Position 4: " + str(d) + ", " + ''.join(str(e) for e in count))
    if (d < 1 or d > 10):
        return False
    if count [d] == 1:
        return False
    count [d] = 1

    # row 3
    # position 5
    e = abs(a-b)
    if debug:
        print ("Position 5: " + str(e) + ", " + ''.join(str(e) for e in count))
    if (e < 1 or e > 10):
        return False
    if count [e] == 1:
        return False
    count [e] = 1

    # position 6
    f = abs (b-c)
    if debug:
        print ("Position 6: " + str(f) + ", " + ''.join(str(e) for e in count))
    if (f < 1 or f > 10):
        return False
    if count [f] == 1:
        return False
    count [f] = 1

    # position 7
    g = abs(c-d)
    if debug:
        print ("Position 7: " + str(g) + ", " + ''.join(str(e) for e in count))
    if (g < 1 or g > 10):
        return False
    if count [g] == 1:
        return False
    count [g] = 1

    # row 2
    # position 8
    h = abs(e-f)
    if debug:
        print ("Position 8: " + str(h) + ", " + ''.join(str(e) for e in count))
    if (h < 1 or h > 10):
        return False
    if count [h] == 1:
        return False
    count [h] = 1

    # position 9
    i = abs(f-g)
    if debug:
        print ("Position 9: " + str(i) + ", " + ''.join(str(e) for e in count))
    if (i < 1 or i > 10):
        return False
    if count [i] == 1:
        return False

    count [i] = 1

    # row 1
    # position 10
    j = abs(h-i)
    if debug:
        print ("Position 10: " + str(j) + ", " + ''.join(str(e) for e in count))
    if (j < 1 or j > 10):
        return False
    if count [j] == 1:
        return False
    # Don't need to do this
    # count [j] = 1
    # print ("Found one")
    return True

# print working numbers, in a triangle format
def print_triangle (a,b,c,d):
    print ("Working numbers: " + str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d))
    print ("      " + str(abs((abs(abs(a-b)-abs(b-c))) - abs(abs(b-c)-abs(c-d)))).center(4))
    print ("    " + str(abs(abs(a-b)-abs(b-c))).center(4) + str(abs(abs(b-c)-abs(c-d))).center(4))
    print ("  " + str(abs(a-b)).center(4) + str(abs(b-c)).center(4) + str(abs(c-d)).center(4))
    print (str(a).center(4) + str(b).center(4) + str(c).center(4) + " " + str(d).center(4))
    print ("")


'''
# not working
check_vals (7,9,4,10)
if check_vals (7,9,4,10):
    print_triangle (7,9,4,10)
# working
if check_vals (8,3,10,9):
    print_triangle (8,3,10,9)
exit()
'''

print ("starting")

for a in range(1,11):
    for b in range (1,11):
        for c in range (1,11):
            for d in range (1,11):
                # print ("Checking numbers: " + str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d))
                if check_vals (a,b,c,d):
                    print_triangle (a,b,c,d)

print ("done")

