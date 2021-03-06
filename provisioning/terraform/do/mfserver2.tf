#terraform plan -var "do_token=..." -out the_plan
#terraform apply the_plan
#terraform show
#terraform destroy -var "do_token=..."

variable "do_token" {}
variable "ssh_key_local_path" {
  default = "./../vb_key.pub"
}
variable "ssh_key_do_name" {
  default = "Victors vb public ssh key"
}


provider "digitalocean" {
  token = "${var.do_token}"
}

resource "digitalocean_ssh_key" "vsemenov_vb_ssh_key" {
    name = "${var.ssh_key_do_name}"
    public_key = "${file("${var.ssh_key_local_path}")}"
}

# Create a web server
resource "digitalocean_droplet" "mfserver2" {
  image = "centos-7-x64"
  name = "mfserver2"
  region = "nyc3"
  size = "2gb"
  user_data = "${file("./../cloud_init.txt")}"
  ssh_keys = ["${digitalocean_ssh_key.vsemenov_vb_ssh_key.id}"]
}


output "ip" {
  value = "${digitalocean_droplet.mfserver2.ipv4_address}"
}
