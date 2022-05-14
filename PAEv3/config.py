from pickle import TRUE


class Config(object):
    #loss = 'focal_loss'
    loss = 'CrossEntropyLoss'
    backbone = 'resnet18'
    classify = 'softmax'
    use_se = False
    easy_margin = False
    num_classes = 10577
    metric = 'arc_margin'
    optimizer = 'sgd'

    web_root = "/home/zhuomengzhang/zhw/PAEv3/CASIA-WebFace"
    web_train_list = "lists/web_train_list.txt"
    AE_train_list = "lists/AE_train_list.txt"
    AE_test_list = "lists/AE_test_pair.txt"

    lfw_root = "./lfw-align-128"
    lfw_train_list = "lists/lfw_train_list.txt"
    lfw_test_list = "lists/lfw_test_pair.txt"
    carrier_list = "lists/lfw_carrier_list.txt"
    carrier_test_list = "lists/carrier_test_pair.txt"

    checkpoints_path = 'checkpoints'
    load_model_path = 'models/resnet18_110.pth'
    test_model_path = 'checkpoints/resnet18_30.pth'

    carrier_num = 100
    AE_num = 50000

    input_shape = (1, 128, 128)
    train_batch_size = 128
    test_batch_size = 60

    print_freq = 500
    save_interval = 10

    max_epoch = 100
    lr = 1e-1  # initial learning rate
    lr_step = 10
    lr_decay = 0.95  # when val_loss increase, lr = lr*lr_decay
    weight_decay = 5e-4

    display = False
    finetune = True

    use_gpu = True  # use GPU or not
    gpu_id = '0,1,2'
    num_workers = 3  # how many workers for loading data