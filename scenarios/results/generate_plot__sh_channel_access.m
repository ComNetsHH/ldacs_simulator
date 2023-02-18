t_slot = 24;

%% Gilbert-Elliot channel model parameters.
p = 0.5; % Transition probability good->bad state.
q = 0.5; % Transition probability bad->good state.
err_1 = 1-(1/exp(1)); % Packet error probability in good state.
err_2 = 1-(1/exp(1)); % Packet error probability in bad state.

target_err_prob = 1-(1/exp(1));
n_contenders = 30;
k = get_candidate_slots(err_1, n_contenders);
n_max_tx_attempts = 5;
max_evaluation_time = n_max_tx_attempts*(k+2);

%% Evaluate Signal Flow Graph.
[x,y] = sh_channel_access(p, q, err_1, err_2, n_contenders, n_max_tx_attempts, err_1, max_evaluation_time);

%% Write to file.
writematrix([x*t_slot; cumsum(y)], ['sfg_mat_' num2str(n_contenders) '.csv']);
disp(['Wrote Signal Flow Graph output to sfg_mat_' num2str(n_contenders) '.csv']);

%% Plot CDF.
figure;
hold on;
ax = gca;
% ax.FontSize = 34; 
set(gca, 'YScale', 'log');
set(gcf, 'color', 'w');
plot(x*t_slot, cumsum(y), 'LineWidth', 1.15);
xlabel('Delay $x$ [ms]', 'interpreter', 'latex');
ylabel('$P(X \leq x)$', 'interpreter', 'latex');
grid on;
hold off;

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