FROM local/c7-systemd
RUN yum -y install sudo; yum clean all;
EXPOSE 80
EXPOSE 443
EXPOSE 8000
CMD ["/usr/sbin/init"]