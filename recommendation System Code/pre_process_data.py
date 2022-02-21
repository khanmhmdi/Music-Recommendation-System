from imblearn.under_sampling import TomekLinks
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import math
import scipy
from sklearn.linear_model import LassoLarsCV
import numpy as np

def data_resampling(X, Y):
    tl = TomekLinks()
    X_tl, y_tl = tl.fit_sample(X, Y)

    return X_tl, y_tl


def remove_outlier(df_in, col_name, first_quartile_length, second_quartile_length):
    for i in col_name:
        q1 = df_in[i].quantile(first_quartile_length)
        q3 = df_in[i].quantile(second_quartile_length)
        iqr = q3 - q1  # Inter quartile range
        fence_low = q1 - 1.5 * iqr
        fence_high = q3 + 1.5 * iqr
        df_in = df_in.loc[(df_in[i] > fence_low) & (df_in[i] < fence_high)]
        print(len(df_in))
    return df_in


def tsne_plot(df):
    plot_kwds = {'alpha': 0.25, 's': 10, 'linewidths': 0}
    projection = TSNE().fit_transform(df)
    return plt.scatter(*projection.T, **plot_kwds)


import math
import scipy
from sklearn.linear_model import LassoLarsCV
def UFS(data, K, d):
    '''
    Cai D, Zhang C, He X. Unsupervised feature selection for multi-cluster data[C]
    //Proceedings of the 16th ACM SIGKDD international conference on Knowledge discovery and data mining. ACM, 2010: 333-342.
    本算法执行的是一个无监督特征选择算法
    data: 是一个N*M的矩阵,每一行代表一个样本,每一列代表一个特征
    K: 聚类的类簇数
    d: 选择的特征数目
    :return :  data:特征选择后的数据N*d 每一行代表一个样本,每一列代表一个特征    seq:表示选择的特征序号1*d,seq中的每一个元素代表原来数据的特征的序号
    '''
    k = int(max(0.2*data.shape[0],10))#近邻设置的数目
    data = np.array(data)
    M = data.shape[1]#数据的维数
    N = data.shape[0]#数据的样本数目
    data = data.transpose()#将矩阵转换成列形式,与文中的形式保持一致
    #寻找数据的样本的K近邻
    dist = np.zeros((N, N))
    delta = 2#原文中热核函数的参数
    W = np.zeros((N, N))#邻接矩阵的权值
    for i in range(N):#计算样本之间的距离
        for j in range(N):
            dist[i,j] = np.linalg.norm(data[:,i]-data[:,j], ord=2)
    D = np.zeros((N, N))#初始化度矩阵
    for i in range(N):#找出每个样本之间的k近邻
        neigbors = np.argsort(dist[i,:], axis=0)
        neigbors = neigbors[1:k+1]#只选取前k个样本,因为第0个最短矩阵是本身与本身的距离,其距离为0
        for j in neigbors:
            W[i,j] = math.exp(-math.pow(np.linalg.norm(data[:,i]-data[:,j]),2)/delta)#计算权值矩阵中的元素
            W[j,i] = W[i,j]
        D[i,i] = sum(W[i,:])#确定度矩阵中的对角元素
    L = D - W #计算拉普拉斯矩阵
    L = L.real
    D = D.real
    feature_values, vectors = scipy.linalg.eig(L,D)#求取Eq.(1)中的广义特征值与特征向量
    feature_values = feature_values.real
    vectors = vectors.real
    seq = np.argsort(feature_values)#对特征值进行排序
    seq = seq[1:K+1]#选取从次小后的K个特征值
    Y = vectors[:,seq]#获取特征向量
    #Y = np.real(Y)
    # 采用最小角回归来气球节a的参数
    score = np.zeros((1,M))#记录每个特征的得分
    model = LassoLarsCV()#训练一个模型
    for i in range(K):
        model.fit(data.transpose(),Y[:,i])
        a = model.coef_#获取线性回归模型的系数
        score[0,i] = max(a)
    seq = np.argsort(-score)#对得分由大到小排序
    seq = seq[0,0:d]#选取前d个最大的得分所对应的特征序号
    data = data.transpose()
    data = data[:,seq]#获得最终的结果
    return data,seq