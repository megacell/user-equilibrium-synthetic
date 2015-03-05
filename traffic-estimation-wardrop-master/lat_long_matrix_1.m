clc;
clear all;

% A coordinates on the small map
% C real coordinates
% D adjusted real coordinates

nodes = [[2.607, 0.930];
    [4.834, 2.068];
    [2.607, 2.447];
    [2.607, 3.426];
    [3.451, 3.377];
    [4.663, 3.573];
    [6.119, 3.475];
    [10.109, 3.842];
    [12.801, 4.184];
    [15.714, 3.879];
    [2.607, 4.539];
    [4.185, 4.625];
    [4.712, 5.139];
    [4.198, 5.604];
    [4.822, 5.763];
    [5.911, 5.616];
    [9.252, 5.555];
    [13.144, 5.543];
    [15.714, 5.004];
    [2.607, 6.277];
    [3.696, 6.191];
    [4.748, 6.411];
    [5.813, 6.252];
    [8.701, 6.301];
    [12.544, 7.109];
    [13.046, 6.546];
    [15.714, 6.387];
    [5.752, 6.729];
    [3.573, 7.512];
    [5.813, 7.512];
    [6.547, 7.512];
    [7.783, 7.512];
    [12.434, 7.512];
    [3.842, 5.371];
    [7.752, 3.511];
    [7.767, 5.371];
    [7.946, 6.133];
    [7.557, 7.104];
    [7.303, 7.515];
    [7.849, 7.276];
    [11.108, 4.183];
    [11.115, 5.378];
    [10.652, 7.208];
    [6.280, 4.192]];

C=[[34.244162,-118.317368];
    [34.208963,-118.219178];
    [34.192210, -118.328128];
    [34.153011, -118.327956];
    [34.152727,-118.284355];
    [34.146476,-118.225358];
    [34.150454,-118.153946];
    [34.132837,-117.958252];
    [34.118626,-117.82573];
    [34.120047,-117.719933];
    [34.107256,-118.331101];
    [34.102992,-118.250023];
    [34.082237,-118.224961];
    [34.063752,-118.24865];
    [34.056642,-118.214318];
    [34.061193,-118.164192];
    [34.065459,-118.000771];
    [34.065743,-117.806107];
    [34.081668,-117.718216];
    [34.03616,-118.331101];
    [34.037867,-118.276277];
    [34.030469,-118.222611];
    [34.03616,-118.170426];
    [34.034453,-118.02829];
    [34.001585, -117.835117];
    [34.02364,-117.812287];
    [34.028193,-117.719246];
    [34.016811,-118.173119];
    [33.975253,-118.282242];
    [33.977531,-118.168366];
    [33.980378,-118.129227];
    [33.984364,-118.074296];
    [33.990057,-117.843583]];

nodes(:,2) = max(nodes(:,2)) - nodes(:,2);

%plot(nodes(:,1),nodes(:,2),'.','MarkerSize',20)

B = [nodes(:,2) nodes(:,1)];

X1 = [ones(44,1) B(:,1)];
X2 = [ones(44,1) B(:,2)];
Y1 = X1(1:33,:);
Y2 = X2(1:33,:);
theta1 = (Y1'*Y1)\(Y1'*C(1:33,1));
theta2 = (Y2'*Y2)\(Y2'*C(1:33,2));

D = [X1*theta1, X2*theta2];

links = [[1,2, 1, 6.0, 1/8.5];
    [2,7, 1, 5.0, 1/9];
    [3,5, 1, 4.0, 1/8.5];
    [4,5, 1, 3.0, 1/10.5];
    [5,6, 1, 3.0, 1/10.5];
    [2,6, 1, 4.0, 1/10.5];
    [6,7, 1, 5.0, 1/10.5];
    [7,35, 1, 5.0, 1/11];
    [35,8, 1, 7.0, 1/11];
    [8,41, 1, 3.0, 1/10.5];
    [41,9, 1, 5.0, 1/10.5];
    [9,10, 1, 7.0, 1/10];
    [5,12, 1, 5.0, 1/9];
    [6,12, 1, 4.0, 1/9];
    [12,13, 1, 3.0, 1/8.5];
    [12,34, 1, 5.0, 1/5];
    [7,44, 1, 5.0, 1/6.5];
    [44,13, 1, 6.0, 1/6.5];
    [13,14, 1, 3.0, 1/9];
    [13,15, 1, 3.0, 1/8.5];
    [8,17, 1, 5.0, 1/8.5];
    [9,18, 1, 4.0, 1/9];
    [11,34, 1, 5.0, 1/8.5];
    [34,14, 1, 2.0, 1/8.5];
    [14,15, 1, 3.0, 1/8];
    [15,16, 1, 4.0, 1/12];
    [16,36, 1, 5.0, 1/9];
    [36,17, 1, 4.0, 1/9];
    [17,42, 1, 5.0, 1/9];
    [42,18, 1, 6.0, 1/9];
    [18,19, 1, 6.0, 1/10.5];
    [14,21, 1, 3.0, 1/8];
    [15,22, 1, 3.0, 1/17];
    [16,23, 1, 2.0, 1/6.5];
    [17,24, 1, 2.0, 1/10.5];
    [18,26, 1, 3.0, 1/9];
    [20,21, 1, 3.0, 1/8.5];
    [21,22, 1, 4.0, 1/10];
    [22,23, 1, 3.0, 1/10.5];
    [23,37, 1, 5.0, 1/10];
    [37,24, 1, 3.0, 1/10]
    [24,43, 1, 6.0, 1/11];
    [43,25, 1, 5.0, 1/11];
    [25,26, 1, 2.0, 1/12];
    [26,27, 1, 7.0, 1/10.5];
    [21,29, 1, 5.0, 1/9];
    [22,28, 1, 4.0, 1/10.5];
    [23,28, 1, 1.5, 1/8.5];
    [28,30, 1, 2.0, 1/11];
    [28,31, 1, 3.0, 1/8.5];
    [24,40, 1, 3.0, 1/10.5];
    [40,32, 1, 1.5, 1/10.5];
    [25,33, 1, 2.0, 1/12];
    [35,36, 1, 9.0, 1/5];
    [36,37, 1, 3.0, 1/7];
    [37,38, 1, 4.0, 1/5];
    [38,39, 1, 2.0, 1/5];
    [38,40, 1, 2.0, 1/5];
    [38,28, 1, 12.0, 1/5];
    [41,42, 1, 8.0, 1/7];
    [42,43, 1, 10.0, 1/7]];
 
dest = 22;
    
ODs = [[2, dest, 6.0]
    [4, dest, 5.0];
    [5, dest, 5.0];
    [6, dest, 2.0];
    [7, dest, 2.0];
    [8, dest, 4.0];
    [9, dest, 3.0];
    [10, dest, 2.0];
    [11, dest, 10.0];
    [17, dest, 4.0];
    [18, dest, 3.0];
    [19, dest, 2.0]
    [20, dest, 10.0];
    [24, dest, 4.0];
    [25, dest, 2.0];
    [26, dest, 2.0];
    [27, dest, 2.0]
    [29, dest, 10.0];
    [30, dest, 10.0];
    [31, dest, 10.0];
    [33, dest, 2.0]];

ODs1 = [ODs(:,1:2), 0.5*ODs(:,3)];
ODs2 = [ODs(:,1:2), 0.8*ODs(:,3)];
ODs3 = ODs;
ODs4 = [ODs(:,1:2), 1.2*ODs(:,3)];
 
ODs1_noisy = [ODs1(:,1:2), normrnd(ODs1(:,3), ODs1(:,3)/30)];
ODs2_noisy = [ODs2(:,1:2), normrnd(ODs2(:,3), ODs2(:,3)/30)];
ODs3_noisy = [ODs3(:,1:2), normrnd(ODs3(:,3), ODs3(:,3)/30)];
ODs4_noisy = [ODs4(:,1:2), normrnd(ODs4(:,3), ODs4(:,3)/30)];

%figure;
%plot(D(:,2),D(:,1),'.','MarkerSize',20)

links = [links; [links(:,2), links(:,1), links(:,3:5)]];
links_noisy = [links(:,1:3), normrnd(links(:,4), links(:,4)/30), links(:,5)];
save('los_angeles_data.mat','nodes','links','ODs1','ODs2','ODs3','ODs4',...
    'links_noisy','ODs1_noisy','ODs2_noisy','ODs3_noisy','ODs4_noisy')