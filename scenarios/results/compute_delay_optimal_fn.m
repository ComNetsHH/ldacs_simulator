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
% along with this program.  If not, see <https:%www.gnu.org/licenses/>.

line_width = 4;
font_size = 26;

syms n q
k(n,q)=1/(1-nthroot(1-q,n));  % no. of candidate slots
d(n,q)=1/(1-q) * (k(n,q)/2);  % expected packet delay
dv=diff(d,q);  % derivative of expected packet delay
fig = figure('visible','off');
hold on;
x = .05:0.01:.95;
n = 100;
y = d(n, x);
writematrix([x; double(y)], 'plot_d.csv');
disp('Wrote plot_d.csv');
%%% The following block plots using Matlab. Above we've saved numerical
%%% results to CSV, which is plotted using plot_delay_optimal_fn.py.
% plot(x, y, 'LineWidth', line_width);
% xline(double(solve(dv(n,q)==0)), 'LineWidth', line_width, 'LineStyle', '--', 'Label', 'minimum', 'fontsize', font_size);
% xticks([0, double(solve(dv(n,q)==0)), 1]);
% xlabel('target collision probability $q$', 'Interpreter', 'latex');
% ylabel('slots', 'Interpreter', 'latex');
% legend({'$d($fixed $n,q)$'}, 'Interpreter','latex', 'Location', 'northoutside', 'Orientation', 'vertical', 'Box','off');
% hold off;
% set(gca, 'FontSize', font_size);
% set(gca, 'TickLabelInterpreter', 'latex');
% set(gca, 'YTick', []);
% set(fig, 'Units', 'Inches');
% pos = get(fig, 'Position');
% set(fig, 'PaperPositionMode', 'Auto', 'PaperUnits', 'Inches', 'PaperSize', [pos(3), pos(4)]);
% print(fig, 'imgs/expected_delay','-dpdf','-r0');
% savefig(fig, 'imgs/expected_delay');
% hold off;

%%% Now for the derivative.
n_max = 200;
y2 = zeros(n_max, 1);
for n=1:n_max
    disp(['Computing derivative ' num2str(n) '/' num2str(n_max)]);
    y2(n) = double(solve(dv(n,q) == 0));
end
writematrix([1:n_max; double(y2')], 'plot_derivative_of_d.csv');
disp('Wrote plot_derivative_of_d.csv');

%%% Uncomment to plot using Matlab.
% fig = figure('visible','off');
% hold on;
% plot(1:n_max, y2, 'LineWidth', line_width);
% yline(1-1/exp(1), 'LineWidth', line_width, 'LineStyle', '--');
% ylim([.5, .65]);
% yticks([.5, 1-1/exp(1)]);
% set(gca, 'YTickLabel', {'0.5', '$1-\frac{1}{e}$'}, 'TickLabelInterpreter', 'latex');
% % set(gca, 'XTick', []);
% ylabel('$q$', 'Interpreter', 'latex');
% ypos = get(ylabel('$q$'), 'Position');
% vf = 1.125; % vertical factor. Adjust manually
% dy = 17; % horizontal offset. Adjust manually
% tpos = get(title(''), 'Position');
% set(ylabel('$q$'), 'Position', [ypos(1)+dy tpos(2)*1.01 ypos(3)], 'Rotation', 0)
% xlabel('number of neighbors $n$', 'Interpreter', 'latex');
% legend({'$\frac{\partial}{\partial q} d(n,q) = 0$'}, 'Interpreter', 'latex', 'Location', 'northoutside', 'Orientation', 'vertical', 'Box','off');
% % set(gca, 'FontSize', font_size);
% % set(fig, 'Units', 'Inches');
% % pos = get(fig, 'Position');
% % set(fig, 'PaperPositionMode', 'Auto', 'PaperUnits', 'Inches', 'PaperSize', [pos(3), pos(4)]);
% % print(fig, 'imgs/expected_delay_derivative','-dpdf','-r0');
% % savefig(fig, 'imgs/expected_delay_derivative');
% hold off;