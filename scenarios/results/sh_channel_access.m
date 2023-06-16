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

function [x, y] = sh_channel_access(p_1, p_2, err_1, err_2, n_contenders, n_max_tx_attempts, q, max_evaluation_time, convolute)
%UNICAST_REQUEST__FUNCTION_OF_X 
%   p_1 -- Gilbert-Elliot transition probability good->bad state.
%   p_2 -- Gilbert-Elliot transition probability bad->good state.
%   err_1 -- Gilbert-Elliot error probability in the good state.
%   err_2 -- Gilbert-Elliot error probability in the bad state.
%   n_contenders -- Number of contenders
%   n_max_tx_attempts -- Maximum number of transmission attempts
%   q -- Target error probability
%   max_evaluation_time -- Number of slots to evaluate up to.
%   convolute -- Whether to convolute the PGF with itself to model two channel accesses (and thus link establishment).
    %% Gilbert-Elliot channel model parameters.
    P = [1-p_1 p_1; p_2 1-p_2]; % Transition probability matrix.
    I = eye(size(P));
    epsilon = [err_1 err_2]; % Error probability vector.
    P0 = I*diag(1-epsilon); % Success probability matrix.
    L = I*diag(epsilon); % Failure probability matrix.
    pi1 = p_2 / (p_1 + p_2); % Steady state distribution: P(good state).
    pi2 = p_1 / (p_2 + p_1); % Steady state distribution: P(bad state).
    pi = [pi1 pi2]; % Steady state distribution.    
    pi_mat = [pi; pi];
    n = n_max_tx_attempts;
    
    syms z; % Delay operator.

    % size of the candidate slot set to achieve the target error probability
    k = get_candidate_slots(q, n_contenders);
    % a random slot is selected from these k candidates under a uniform
    % selection probability  %z^((1/k) * (((k*(k+1)) / 2)))
    G_slot = 0;
    for i=1:k
        G_slot = G_slot + (1/k) * z^i;
    end
    % transmission takes one time slot
    G_tx = z^1;

    % construct probability generating function
    t = P*G_slot*G_tx; % select slot, then transmit
    s = (I-L); % probability of successful transmission
    f = L; % probability of a dropped packet
    G_failure = f^n * t^n;
    G_success = 0;
    for i=1:n
        G_success = G_success + t^i * f^(i-1) * s;
    end
    G = pi_mat * (G_failure + G_success);

    %% Evaluate.
    use_taylor = 1; % Whether to use the Taylor power series, which is much faster than finding the derivatives directly.
    pgf_to_evaluate = pi_mat;
    if convolute == 0
        pgf_to_evaluate = pgf_to_evaluate * G_success;
    else
        pgf_to_evaluate = pgf_to_evaluate * (G_success * G_success);  % multiplication in the z-domain is convolution in discrete-time-domain
    end
    [x,y] = evaluate_pgf(pgf_to_evaluate , pi, P, use_taylor, max_evaluation_time, 1);
end

