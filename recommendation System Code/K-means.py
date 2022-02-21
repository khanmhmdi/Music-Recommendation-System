import matplotlib
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score

class K_means(object):
    def k_means(X, Y):
        kmeans = KMeans(n_clusters=12, random_state=0)

        kmeans.fit(X)

        labels = kmeans.labels_
        # check how many of the samples were correctly labeled

        return labels

    def get_accuracy(Y_pred, Y_true ):
        return accuracy_score(Y_pred, Y_true)

    def plot_clusters(self , labels , data , cluster_list):
        filtered_lables = []
        for i in cluster_list:
            filtered_lable = data[labels == i]
            filtered_lables.append(filtered_lable)
        # filtered_label2 = data[labels == 2]

        # filtered_label8 = data[labels == 1]

        # Plotting the results
        # plt.scatter(filtered_label2.iloc[:, 0], filtered_label2.iloc[:, 1], color='red')
        # plt.scatter(filtered_label8.iloc[:, 0], filtered_label8.iloc[:, 1], color='black')
        colors = ['red' , 'blue' , 'black' , 'black' , 'green' , 'ornage' , 'purple' , 'gray' ]

        for  i in cluster_list:
            plt.scatter(i.iloc[:, 0], i.iloc[:, 1], color=colors[i])
        return plt.show()

