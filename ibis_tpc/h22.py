def tpc_h22(con, COUNTRY_CODES=('13', '31', '23', '29', '30', '18', '17')):
    '''Global Sales Opportunity Query (Q22)

    The Global Sales Opportunity Query identifies geographies where there are
    customers who may be likely to make a purchase.'''

    customer = con.table('customer')
    orders = con.table('orders')

    q = customer.filter([
        customer.C_ACCTBAL > 0.00,
        customer.C_PHONE.substr(0, 2).isin(COUNTRY_CODES),
    ])
    q = q.aggregate(avg_bal=customer.C_ACCTBAL.mean())

    custsale = customer.filter([
        customer.C_PHONE.substr(0, 2).isin(COUNTRY_CODES),
        customer.C_ACCTBAL > q.avg_bal,
        ~(orders.O_CUSTKEY == customer.C_CUSTKEY).any()
    ])
    custsale = custsale[
        customer.C_PHONE.substr(0, 2).name('cntrycode'),
        customer.C_ACCTBAL
    ]

    gq = custsale.group_by(custsale.cntrycode)
    outerq = gq.aggregate(numcust=custsale.count(),
                          totacctbal=custsale.C_ACCTBAL.sum())

    return outerq.sort_by(outerq.cntrycode)
