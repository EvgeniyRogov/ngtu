t = 0:pi/100:2*pi;

R = 1;
x_ball = 0;
y_ball = 0;

X = -10:0.01:10;
Y = X.^2;

F = figure;
Pr = plot(X,Y);
hold on;
P_ball = plot(x_ball,y_ball,'o');
axis equal;
ylim([-1 10]);
xlim([-10 10]);

clock = 0;
h = 0.01;
z = [];
z(1) = 0;
x = [];
x(1) = -3;
i = 1;
while isvalid(F)
    pause(0.01);
 
    k1 = h * f(clock,x(i),z(i));
    m1 = h * g(clock,x(i),z(i));
    k2 = h * f(clock + h / 2, x(i) + k1 / 2,z(i) + m1 / 2);
    m2 = h * g(clock + h / 2, x(i) + k1 / 2,z(i) + m1 / 2);
    k3 = h * f(clock + h / 2, x(i) + k2 / 2,z(i) + m2 / 2);
    m3 = h * g(clock + h / 2, x(i) + k2 / 2,z(i) + m2 / 2);
    k4 = h * f(clock + h, x(i) + k3, z(i) + m3);
    m4 = h * g(clock + h, x(i) + k3, z(i) + m3);
    x(i + 1) = x(i) + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
    z(i + 1) = z(i) + (m1 + 2 * m2 + 2 * m3 + m4) / 6;
    
    px = x_ball + x(i);
    py = y_ball + px.^2;
    set(P_ball,'XData',px);
    set(P_ball,'YData',py);
    drawnow
    clock = clock + h;
    i = i + 1;
end

