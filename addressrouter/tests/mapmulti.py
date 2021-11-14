import simplemulti
import addressrouter.maputil as mu

testnum = 4
result = simplemulti.run_multivehicle(testnum)

for route_solution in result[3]:
    print(mu.genmapslink(route_solution))