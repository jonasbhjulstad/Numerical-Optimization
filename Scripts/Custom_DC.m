import casadi.*

d = 3;
tau = collocation_points(d);

[C,D,B] = collocation_coeff(tau);

T = 10;
x1 = SX.sym('x1');
x2 = SX.sym('x2');
x = [x1; x2];
u = SX.sym('u');

xdot = [(1-x2^2)*x1 - x2 + u; x1];

L = x1^2 + x2^2 + u^2;

f = Function('f', {x, u}, {xdot, L});

N = 20;
h = T/N;

opti = Opti();
J = 0;

Xk = opti.variable(2);
opti.subject_to(Xk==[0; 1]);
opti.set_initial(Xk, [0; 1]);

Xs = {Xk};
Us = {};

for k = 0:N-1
    Uk = opti.variable();
    Us{end+1} = Uk;
    opti.subject_to(-1 <= Uk <= 1);
    opti.set_initial(Uk, 0);
    
    Xc = opti.variable(2, d);
    opti.subject_to(-0.25 <= Xc(1,:));
    opti.set_initial(Xc, repmat([0;0], 1, d));
    
    [ode, quad] = f(Xc, Uk);
    
    J = J + quad*B*h;
    
    Z = [Xk Xc];
    
    Pidot = Z*C;
    
    opti.subject_to(Pidot == h*ode); 
    Xk_end = Z*D;
    
    Xk = opti.variable(2);
    Xs{end + 1} = Xk;
    opti.subject_to(-0.25 <= Xk(1));
    opti.set_initial(Xk, [0;0]);
    opti.subject_to(Xk_end == Xk);
end
Xs = [Xs{:}];
Us = [Us{:}];

opti.minimize(J);
opti.solver('ipopt');
sol = opti.solve();

x_opt = sol.value(Xs);