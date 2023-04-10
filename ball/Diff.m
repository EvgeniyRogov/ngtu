function [ res ] = Diff( x_der )
    load C:\Users\hp\desktop\Matlab\Ball\my_graphic;
    h = 0.01;
    res = (spline(x, y, x_der + h) - spline(x, y, x_der - h)) / (2 * h);
end

