function [ res ] = g( t,p,z )
    g = 9.81;
    b = 0.06;
    res = -g*Diff(p)-b*z;
end

