function [ X S ] = Spline( div )

load C:\Users\hp\desktop\Matlab\Ball\my_graphic;

step = 2*div;
xi = 0:step:200;
N = length(xi);

for i = 1:1:N
   yi(i) = Conform(xi(i)); 
end


for i = 1 : 1 : N-1
    hi(i) = xi(i + 1) - xi(i);
end


for i = 1 : 1 : N-1
    delta1(i) = (yi(i+1)-yi(i)) / (xi(i+1)-xi(i));
end


for i = 1 : 1 : N-2
    delta2(i) = (delta1(i+1)-delta1(i)) / (xi(i+2)-xi(i));
end


for i = 1 : 1 : N-3
    delta3(i) = (delta2(i+1)-delta2(i)) / (xi(i+3)-xi(i));
end

A = zeros(N);

A(1,1) = -hi(1);

for i = 2 : 1 : N-1
    A(i,i) = 2*(hi(i-1)+hi(i)); 
end

A(N,N) = -hi(N-1);

for i = 2 : 1 : N
    A(i-1,i) = hi(i - 1); 
    A(i,i-1) = hi(i - 1); 
end

C(1) = hi(1)*hi(1)*delta3(1);
for i = 2 : 1 : N-1
   C(i) = delta1(i) - delta1(i-1); 
end
C(N) = -hi(N-1)*hi(N-1)*delta3(N-3);
C = C';

P = A\C;
S = [];
X = [];

for i = 1:1:N-1
    a(i) = yi(i);
    b(i) = (yi(i+1) - yi(i))/ hi(i) - hi(i)*(P(i+1) + 2*P(i));
    c(i) = 3 * P(i);
    d(i) = (P(i+1) - P(i)) / hi(i);
    xx = xi(i):0.01:xi(i+1);
    for k = 1 : 1 : length(xx)
        X(end + 1) = xx(k);
        S(end + 1) = a(i) + b(i)*(xx(k) - xi(i)) + c(i)*(xx(k) - xi(i))^2 + d(i)*(xx(k) - xi(i))^3;
    end    
end

end

