load C:\Users\hp\desktop\Matlab\Ball\my_graphic;
F = figure;
x_ball = 0;
y_ball = 0;

[X Y] = Spline(1);

subplot(1,2,1);
Pr = plot(X,Y);
hold on;
P_ball = plot(x_ball,y_ball,'o');
title('Ball');
grid on;
xlabel('X');
ylabel('Y');

t = 0;
dt = 0.1;
z = [];
z(1) = 0; 
p = [];
p(1) = 180; 
i = 1;

while isvalid(F)
 
    k1 = dt * f(t,p(i),z(i));
    m1 = dt * g(t,p(i),z(i));
    k2 = dt * f(t + dt / 2, p(i) + k1 / 2,z(i) + m1 / 2);
    m2 = dt * g(t + dt / 2, p(i) + k1 / 2,z(i) + m1 / 2);
    k3 = dt * f(t + dt / 2, p(i) + k2 / 2,z(i) + m2 / 2);
    m3 = dt * g(t + dt / 2, p(i) + k2 / 2,z(i) + m2 / 2);
    k4 = dt * f(t + dt, p(i) + k3, z(i) + m3);
    m4 = dt * g(t + dt, p(i) + k3, z(i) + m3);
    p(i + 1) = p(i) + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
    z(i + 1) = z(i) + (m1 + 2 * m2 + 2 * m3 + m4) / 6;
    px = x_ball + p(i);
    if px < 0 | px > 200
        break
    end
    py = y_ball + spline(x,y,px);
    set(P_ball,'XData',px);
    set(P_ball,'YData',py);
    
    subplot(1,2,2); 
    plot(p,z);
    xlim([0 200]);
    ylim([-50 50]);
    title('V(X)');
    grid on;
    xlabel('X');
    ylabel('V');
    
    if(abs(z(i+1)) < 0.001) 
        break
    end
    
    drawnow
    t = t + dt;
    i = i + 1;
end
