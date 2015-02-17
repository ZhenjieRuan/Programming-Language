# ####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 4 (skeleton code)
# interpret.py
#
exec(open("parse.py").read())

Leaf = str
Node = dict

def getLabel(dic):
    for label in dic:
        return label


def subst(s, a):
    if type(a) == Node:
        label = getLabel(a)
        children = a[label]
        if label != "Variable":
            return {label: [subst(s, a) for a in children]}

        v = children[0]
        try:
            return s[v]
        except:
            return a
    elif type(a) == Leaf or type(a) == int:
        return a


def unify(a, b):
    if a == b and (type(a) == Leaf or type(a) == int):    return {}
    if type(a) == type(b) == Node:
        aL, bL = getLabel(a), getLabel(b)
        if "Variable" in [aL, bL]:
            return {a[aL][0]: b} if aL == "Variable" else {b[bL][0]: a}
        if aL == bL and len(a[aL]) == len(b[bL]):
            aC, bC, u = a[aL], b[bL], []
            for x, y in zip(aC, bC): #pair aC and bC
                try:
                    u += list(unify(x, y).items())
                except:
                    pass
            return dict(u)


def build(m, d):
    if type(d) == Node:
        label = getLabel(d)
        children = d[label]

        if label == "Function":
            name = children[0]['Variable'][0]
            if name not in m:
                n1 = children[1]
                n2 = children[2]
                m[name] = [(n1,n2)]
            else:
                n1 = children[1]
                n2 = children[2]
                m[name] += [(n1,n2)]
            return build(m, children[3])

    elif type(d) == Leaf and d == "End":
        return m


def evaluate(m, env, e):
    label = getLabel(e)
    children = e[label]

    if label == "ConInd":
        e1 = children[1]
        e2 = children[2]
        v1 = evaluate(m,env,e1)
        v2 = evaluate(m,env,e2)
        children[1] = v1
        children[2] = v2
        return e

    if label == "ConBase" or label == "Number":
        return e

    if label == "Variable":
        v = children[0]
        if v in env:
            return env[v]
    if label == "Number":
        return children[0]

    if label == "Plus":
        v1 = evaluate(m, env, children[0])
        v2 = evaluate(m, env, children[1])
        return v1 + v2

    if label == "Apply":
        f = children[0]['Variable'][0]
        v1  = evaluate(m, env, children[1])
        for i in m[f]:
            u = unify(v1, i[0])
            if subst(u, v1) == subst(u, i[0]): 
                return evaluate(m, u, i[1])


def interact(s):
    # Build the module definition.
    m = build({}, parser(grammar, 'declaration')(s))

    # Interactive loop.
    while True:
        # Prompt the user for a query.
        s = input('> ')
        if s == ':quit':
            break

        # Parse and evaluate the query.
        e = parser(grammar, 'expression')(s)
        if not e is None:
            print(evaluate(m, {}, e))
        else:
            print("Unknown input.")

            #eof