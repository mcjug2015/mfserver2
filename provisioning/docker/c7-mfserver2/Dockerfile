FROM local/c7-systemd
RUN yum -y install sudo; yum clean all;
EXPOSE 80
EXPOSE 443
CMD ["/usr/sbin/init"]