#### List
from mock_data import mock_catalog

def test_1():
    print("basic python lists")

    nums = [1,2,3,4,5,6,776,8998,000,543,66]
    
    #read
    print(nums[0])
    print(nums[3])

    # add
    nums.append(42)
    nums.append(343)

    #remove by element
    nums.remove(776)

    #remove by index
    del nums[2]

    print(nums)

    #loop
    for n in nums:
        print(n)

def test_2():

    print("Sum numbers")

    prices = [12.23,345,123.2,542,65,123.2,0.223,-23, 123.2,6,171,5678]

    # for and print every number
    total = 0
    cheapest= prices[0]
    expensive= prices[1]
    for num in prices:
        total += num
        if num < cheapest:
            cheapest = num

        if num > expensive:
            expensive = num
            
    print(total)
    print(f"The cheapest price is: {cheapest}")
    print(f"The most expensive price is: {expensive}")
           
def test_3():
    print("cheapest product")

    cheap_prod= mock_catalog[0]
    for prod in mock_catalog:
        if prod["unitPrice"] < cheap_prod["unitPrice"]:
            cheap_prod = prod

        
    print(prod["title"])
    print(f"The cheapest price is: {cheap_prod['title']} - ${cheap_prod['unitPrice']}")

#call py test2.py
#test_1()
#test_2()
test_3()