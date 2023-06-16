% The L-Band Digital Aeronautical Communications System (LDACS) simulator provides an installation script for the simulator that downloads the other simulator components, defines simulation scenarios and provides result evaluation and graph creation.
% Copyright (C) 2023  Sebastian Lindner, Konrad Fuger, Musab Ahmed Eltayeb Ahmed, Andreas Timm-Giel, Institute of Communication Networks, Hamburg University of Technology, Hamburg, Germany
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU Lesser General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU Lesser General Public License for more details.
%
% You should have received a copy of the GNU Lesser General Public License
% along with this program.  If not, see <https://www.gnu.org/licenses/>.

function [xVec, pmfVec] = evaluate_pgf(G, steady_state_distribution, P, use_taylor_approx, max_eval_time, scalarize)
    syms z;
    % Transform to scalar PGF.    
    if scalarize > 0
        G = (steady_state_distribution * G * ones(size(P,1), 1)) / (steady_state_distribution * ones(size(P,1), 1));
    end
    % Evaluate
    if use_taylor_approx
        taylor_series = sym2poly(taylor(G, 'Order', max_eval_time));        
        taylor_series = fliplr(taylor_series);           
        taylor_series = taylor_series(2:end); % first derivative is in 2nd summand.        
        disp('sum=' + string(sum(taylor_series)));
        if sum(taylor_series) > 1
            disp('Sum of Taylor series is larger than one: ' + string(sum(taylor_series)) + ' -> Normalizing values to this sum.');            
            taylor_series = taylor_series./sum(taylor_series);
        end        
        pmfVec = [taylor_series zeros(1, max_eval_time - length(taylor_series))];
        xVec = 1:length(pmfVec); 
    else
        xVec = 0:1:max_eval_time;    
        pmfVec = zeros(size(xVec)); % Holds probability mass function values.
        current_derivative = symfun(G, z); % Working copy for current derivative of G(z).        
        for transmission_time = 0:1:max_eval_time            
            disp('Progress: ' + string(transmission_time / max_eval_time * 100) + '%');            
            % Derive for z.
            current_derivative = diff(current_derivative, z);
            % Transform to PMF through 1/k! * derivative(z=0).                        
            k = 1 + transmission_time;        
            current_derivative(0)
            pmf = 1/factorial(k) * current_derivative(0);        
            pmfVec(1 + transmission_time) = pmf;         
        end           
    end
end

