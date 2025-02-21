# vpc network
resource "yandex_vpc_network" "network" {
  name = "practix-network"
}

# vpc subnet
resource "yandex_vpc_subnet" "subnet_d" {
  name           = "practix-subnet-d"
  zone           = "ru-central1-d"
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["10.5.0.0/24"]
  depends_on     = [yandex_vpc_network.network]
  route_table_id = yandex_vpc_route_table.rt.id
}

# vpc gateway
resource "yandex_vpc_gateway" "nat_gateway" {
  name = "practix-gateway"
  shared_egress_gateway {}
}

# vpc route table
resource "yandex_vpc_route_table" "rt" {
  name       = "practix-route-table"
  network_id = yandex_vpc_network.network.id

  static_route {
    destination_prefix = "0.0.0.0/0"
    gateway_id         = yandex_vpc_gateway.nat_gateway.id
  }
}

output "network" {
  value       = yandex_vpc_network.network
}

output "subnet_d" {
  value       = yandex_vpc_subnet.subnet_d
}

output "nat_gateway" {
  value       = yandex_vpc_gateway.nat_gateway
}

output "route_table" {
  value       = yandex_vpc_route_table.rt
}
