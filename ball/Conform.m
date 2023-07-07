function out_y = Conform(arg_x)

    if(arg_x < 0 || arg_x > 200)
        disp('Error');
        return
    end

    load C:\Users\hp\desktop\Matlab\Ball\my_graphic;

    if mod(arg_x,2) == 0
        i = 1;
        while 1,
            if x(i) == arg_x
                out_y = y(i);
                return
            end
            i = i + 1;
        end
    elseif floor(arg_x) == arg_x
        x1 = arg_x - 1;
        x2 = arg_x + 1;
    else
        if mod(floor(arg_x),2) == 0
            x1 = floor(arg_x);
            x2 = x1 + 2;
        else
            x2 = ceil(arg_x);
            x1 = x2 - 2;
        end

    end

    i = 1;

    while 1,
        if x(i) == x1
            y1 = y(i);
            break
        end
        i = i + 1;
    end

    y2 = y(i + 1);

    k = (y1-y2)/(x1-x2);
    b = y2 - k*x2;
    out_y = k * arg_x + b;

end
