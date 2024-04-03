import math
import sympy as sp

constants = {
    'sigma': 1+math.sqrt(2),
    'epsilon': 1-math.sqrt(2),
    'R': 83.14,
    'Omega': 0.07780,
    'Psi': 0.45724,
    'alpha': lambda Tr, w: (1+(0.37464+1.54226*w-0.26992*w**2)*(1-math.sqrt(Tr)))**2 \
              if w <= 0.491 else (1+(0.379642+1.487503*w-0.164423*w**2+0.016666*w**3)*(1-math.sqrt(Tr)))**2
}

species = [
    {
        'Tc': 508.2,
        'omega': 0.307,
        'Pc': 47.01,
    },
    {
        'Tc': 508.3,
        'omega': 0.668,
        'Pc': 47.62,
    }
]
import math
import sympy as sp

def PR(Pressure, xMoleFrac, Temperature, yMoleFrac, TStep, maxIter):

    ySum = 0
    j = 1
    prevStep = 0
    while abs(ySum - 1) > 0.0001 and j <= maxIter:
        for i in range(2):
            Tc = species[i]['Tc']
            Pc = species[i]['Pc']
            Tr = Temperature / Tc
            alpha = constants['alpha'](Tr, species[i]['omega'])
            species[i]['a'] = constants['Psi'] * alpha * constants['R'] ** 2 * Tc ** 2 / Pc
            species[i]['b'] = constants['Omega'] * constants['R'] * Tc / Pc

        x1, x2 = xMoleFrac, 1 - xMoleFrac
        y1, y2 = yMoleFrac, 1 - yMoleFrac

        a1, a2 = species[0]['a'], species[1]['a']
        b1, b2 = species[0]['b'], species[1]['b']

        vle = {
            'liquid': {
                'a': x1 ** 2 * a1 + 2 * x1 * x2 * math.sqrt(a1 * a2) + x2 ** 2 * a2,
                'b': x1 * b1 + x2 * b2
            },
            'vapor': {
                'a': y1 ** 2 * a1 + 2 * y1 * y2 * math.sqrt(a1 * a2) + y2 ** 2 * a2,
                'b': y1 * b1 + y2 * b2
            }
        }

        vle['liquid']['a1Bar'] = 2 * x1 * a1 + 2 * x2 * math.sqrt(a1 * a2) - vle['liquid']['a']
        vle['liquid']['a2Bar'] = 2 * x2 * a2 + 2 * x1 * math.sqrt(a1 * a2) - vle['liquid']['a']
        vle['vapor']['a1Bar'] = 2 * y1 * a1 + 2 * y2 * math.sqrt(a1 * a2) - vle['vapor']['a']
        vle['vapor']['a2Bar'] = 2 * y2 * a2 + 2 * y1 * math.sqrt(a1 * a2) - vle['vapor']['a']

        # Solve PR equations for vapor and liquid
        for phase in vle.keys():
            a, b = vle[phase]['a'], vle[phase]['b']
            B = b * Pressure / (constants['R'] * Temperature)
            A = a *alpha*Pressure /constants['R']**2 / Temperature **2 
            Z = sp.symbols('Z')
            q = a / (b * constants['R'] * Temperature)
            equation = Z **3 - (1-B) * Z **2 + (A-2*B-3*B**2)*Z-(A*B-B**2-B**3)
            solution = sp.solve(equation, Z)
            if phase == 'vapor':
                z = sp.re(solution[-1])
            else:
                z = sp.re(solution[0])

            I = (math.log(z + constants['sigma'] * B) - math.log(z + constants['epsilon'] * B)) / (
                        constants['sigma'] - constants['epsilon'])

            vle[phase]['B'] = B
            vle[phase]['q'] = q
            vle[phase]['z'] = z
            vle[phase]['I'] = I

            for i in range(2):
                aiBar, bi = vle[phase][f'a{i + 1}Bar'], species[i]['b']
                qiBar = q * (1 + aiBar / a - bi / b)
                phi = math.exp(bi / b * (z - 1) - math.log(z - B) - qiBar * I)

                vle[phase][f'q{i + 1}Bar'] = qiBar
                vle[phase][f'phi{i + 1}'] = phi

        for i in range(2):
            species[i]['K'] = vle['liquid'][f'phi{i + 1}'] / vle['vapor'][f'phi{i + 1}']

        y1Final = species[0]['K'] * x1
        y2Final = species[1]['K'] * x2
        ySum = y1Final + y2Final

        # Update
        if ySum > 1.0001:
            TStep = -abs(TStep)
        elif ySum < 0.9999:
            TStep = abs(TStep)

        if prevStep * TStep < 0:
            TStep /= 2


        Temperature += TStep
        yMoleFrac = y1Final / ySum
        j += 1
        prevStep = TStep

    return Temperature, y1Final, y2Final


if __name__ == "__main__":
    xList = [0.092027467, 0.150737506, 0.233719893, 0.340767172]
    YList = [0.357, 0.480, 0.588, 0.673]
    TList = [346.512,342.835, 339.194, 336.124]
    tResultList = []
    y1ResultList = []
    y2ResultList = []
    for x, y, t in zip(xList, YList, TList):
        tResult, y1, y2 = PR(1, x,t, y, 20, 100000)
        tResultList.append(tResult)
        y1ResultList.append(y1)
        y2ResultList.append(y2)
    print("X1       Y1       Y2       T")
    for t, x1, y1, y2 in zip(tResultList, xList, y1ResultList, y2ResultList):
        print(f"{x1:.4f}   {y1:.4f}   {y2:.4f}   {t:.4f}")

