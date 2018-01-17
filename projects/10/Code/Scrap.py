def test_re(test,string):
    m1=test.match(string)
    print m1.group(m1.lastindex)
    print m1.lastindex