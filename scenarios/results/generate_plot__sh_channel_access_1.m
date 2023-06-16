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

n_contenders = 10;
t_slot = 24;

%% Gilbert-Elliot channel model parameters.
p = 1.0; % Transition probability good->bad state.
q = 1.0; % Transition probability bad->good state.
err_1 = 1-(1/exp(1)); % Packet error probability in good state.
err_2 = 1-(1/exp(1)); % Packet error probability in bad state.

target_err_prob = 1-(1/exp(1));
k = get_candidate_slots(target_err_prob, n_contenders);
n_max_tx_attempts = 15;
max_evaluation_time = n_max_tx_attempts*(k+2);

%% Evaluate Signal Flow Graph.
convolute = 0;
[x,y] = sh_channel_access(p, q, err_1, err_2, n_contenders, n_max_tx_attempts, target_err_prob, max_evaluation_time, convolute);

%% Write to file.
writematrix([x; y], ['sfg_mat_' num2str(n_contenders) '.csv']);
disp(['Wrote Signal Flow Graph output to sfg_mat_' num2str(n_contenders) '.csv']);
%% Plot CDF.
% figure;
% hold on;
% ax = gca;
% % ax.FontSize = 34; 
% set(gca, 'YScale', 'log');
% set(gcf, 'color', 'w');
% plot(x*t_slot, cumsum(y), 'LineWidth', 1.15);
% xlabel('Delay $x$ [ms]', 'interpreter', 'latex');
% ylabel('$P(X \leq x)$', 'interpreter', 'latex');
% grid on;
% hold off;

%% Plot CCDF.
% figure;
% hold on;
% ax = gca;
% ax.FontSize = 34; 
% set(gca, 'YScale', 'log');
% set(gcf, 'color', 'w');
% plot(x*t_slot, 1-cumsum(y), 'LineWidth', 1.15);
% xlabel('Delay $x$ [ms]', 'interpreter', 'latex');
% ylabel('$P(X>x)$', 'interpreter', 'latex');
% grid on;
% hold off;