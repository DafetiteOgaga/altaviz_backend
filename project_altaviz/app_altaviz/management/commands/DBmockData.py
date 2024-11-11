import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.db.models import Q
from app_users.models import User, Region
from app_location.models import Location
from app_custodian.models import Branch, Custodian, RequestDetailsChange
from app_bank.models import Bank, State
from app_contactus.models import ContactUs
from app_fault.models import FaultName, Fault
from app_inventory.models import ComponentName, Component, PartName, Part, RequestPart, RequestComponent, UnconfirmedPart

class Command(BaseCommand):
	help = 'Populate the database with fake data'

	def handle(self, *args, **kwargs):
		fake = Faker()
		check = User.objects.all()

		# Create 10 states
		states = [State.objects.create(name=fake.state()) for _ in range(10)]

		# Create 3 regions
		regions = []
		for i in range(3):
			region = Region.objects.create(name=f'Region_{i + 1}')
			regions.append(region)

			# Create 4 engineers for each region
			for j in range(4):
				if check.filter(username=f'engineer_{i + 1}{j + 1}').exists(): continue
				User.objects.create_user(
					username=f'engineer_{i + 1}{j + 1}',
					email=f'engineer{i + 1}{j + 1}@engineer.com',
					first_name=f'engineerFname_{i + 1}{j + 1}',
					last_name=f'engineerLname_{i + 1}{j + 1}',
					middle_name=f'engineerMname_{i + 1}{j + 1}',
					gender=random.choice(['male', 'female']),
					date_of_birth=fake.date_of_birth(minimum_age=24, maximum_age=50),
					wphone=fake.phone_number(),
					password='password123',  # In production, use a hashed password
					role='engineer',
					phone=fake.phone_number(),
					address=fake.address(),
					region=region
				)

			# Create 3 help-desk and supervisor users for each region
			for role in ['help-desk', 'supervisor']:
				for k in range(3):
					if check.filter(username=f'{role}_{k + 1}').exists(): continue
					currRole = User.objects.create_user(
							username=f'{role}_{k + 1}',
							email=f'{role}{k + 1}@{role}.com',
							first_name=f'{role}Fname_{k + 1}',
							last_name=f'{role}Lname_{k + 1}',
							middle_name=f'{role}Mname_{k + 1}',
							gender=random.choice(['male', 'female']),
							date_of_birth=fake.date_of_birth(minimum_age=24, maximum_age=50),
							wphone=fake.phone_number(),
							password='password123',  # In production, use a hashed password
							role=role,
							phone=fake.phone_number(),
							address=fake.address(),
							region=region
						)
		# print(f'current user: {currRole.first_name}')
		# for reg in regions:
		regionalUsers = list(User.objects.filter(Q(role='help-desk') | Q(role='supervisor')))
		# print(f'regionUsers: {regionalUsers}')
		[print(f'user: {user}') for user in regionalUsers]
		hcount = 0
		scount = 0
		rcount = 0
		for user in regionalUsers:
			if user.role == 'help-desk':
				print('11111111111111111')
				print(f'user: {user.first_name}')
				print(f'region: {regions[hcount]}')
				regions[hcount].helpdesk = user
				user.region = regions[hcount]
				rcount = hcount
				hcount += 1
			else:
				print('22222222222222222')
				print(f'user: {user.first_name}')
				print(f'region: {regions[scount]}')
				regions[scount].supervisor = user
				user.region = regions[scount]
				rcount = scount
				scount += 1
			print(f'assigning {user.role}: ({user.first_name}) user to {regions[rcount]} region field')
			user.save()
			regions[rcount].save()
			print(f'{user.first_name} added to {regions[rcount]} region field and user region changed to {regions[rcount]}')

		# Create 1 HR user
		if not check.filter(username=f'hr_user').exists():
			hr_user = User.objects.create_user(
				username='hr_user',
				email='hr@human-resource.com',
				first_name=f'human-resourceFname_{i + 1}{j + 1}',
				last_name=f'human-resourceLname_{i + 1}{j + 1}',
				middle_name=f'human-resourceMname_{i + 1}{j + 1}',
				gender=random.choice(['male', 'female']),
				date_of_birth=fake.date_of_birth(minimum_age=24, maximum_age=50),
				wphone=fake.phone_number(),
				password='password123',  # In production, use a hashed password
				role='human-resource',
				phone=fake.phone_number(),
				address=fake.address(),
				region=random.choice(regions)  # Randomly assign to any region
			)

		# Create 15 locations
		locations = [Location.objects.create(
			location=fake.city(),
			state=random.choice(states),  # Assign random state to location
			region=random.choice(regions)
		) for _ in range(15)]

		# Create 12 banks
		banks = []
		for _ in range(12):
			bank = Bank.objects.create(name=fake.company())
			# Associate the bank with 1 to 5 random states
			bank.states.set(random.sample(states, random.randint(1, 5)))  # Choose random states
			banks.append(bank)

		# Create 14 branches
		for _ in range(14):
			Branch.objects.create(
				name=fake.company_suffix(),
				bank=random.choice(banks),
				location=random.choice(locations)
			)

		# Create sample ContactUs entries
		for _ in range(10):
			ContactUs.objects.create(
				name=fake.name(),
				email=fake.email(),
				message=fake.sentence(nb_words=10)
			)

		# Create 2 custodians
		for _ in range(2):
			user = User.objects.create_user(
				username=fake.user_name(),
				email=fake.email(),
				first_name=f'custodianFname_{i + 1}{j + 1}',
				last_name=f'custodianLname_{i + 1}{j + 1}',
				middle_name=f'custodianMname_{i + 1}{j + 1}',
				gender=random.choice(['male', 'female']),
				date_of_birth=fake.date_of_birth(minimum_age=24, maximum_age=50),
				wphone=fake.phone_number(),
				password='password123',  # In production, use a hashed password
				role='custodian',
				region=random.choice(regions)  # Randomly assign to any region
			)
			branch = random.choice(Branch.objects.all())
			Custodian.objects.create(email=user, branch=branch)

			# Create 2 RequestDetailsChange for each custodian
			for _ in range(2):
				RequestDetailsChange.objects.create(
					email=user,
					state=fake.state(),
					branch=branch.name,
					location=fake.city(),
					status=False
				)

		# Create 10 FaultNames
		fault_names = [FaultName.objects.create(name=fake.sentence(nb_words=2)) for _ in range(10)]

		# Create 50 Faults
		for _ in range(50):
			fault_name = random.choice(fault_names)
			location = random.choice(locations)
			assigned_to = random.choice(User.objects.filter(role='engineer'))
			managed_by = random.choice(User.objects.filter(role='help-desk'))
			supervisor = random.choice(User.objects.filter(role='supervisor'))
			logged_by = random.choice(Custodian.objects.all())
			Fault.objects.create(
				title=fault_name,
				location=location,
				assigned_to=assigned_to,
				managed_by=managed_by,
				supervised_by=supervisor,
				logged_by=logged_by,
				other=fake.text(),
				confirm_resolve=random.choice([True, False]),
				verify_resolve=random.choice([True, False]),
			)

		# Create 12 ComponentNames
		component_names = [ComponentName.objects.create(name=fake.word()) for _ in range(12)]

		# Create 15 Components
		for _ in range(15):
			Component.objects.create(
				name=random.choice(component_names),
				quantity=random.randint(0, 500),
				user=random.choice(User.objects.filter(role='human-resource'))
			)

		# Create 9 PartNames
		part_names = [PartName.objects.create(name=fake.word()) for _ in range(9)]

		# Create 17 Parts
		for _ in range(17):
			Part.objects.create(
				name=random.choice(part_names),
				quantity=random.randint(0, 500),
				user=random.choice(User.objects.filter(role='human-resource'))
			)

		# Create 21 RequestParts
		for _ in range(21):
			RequestPart.objects.create(
				name=random.choice(part_names),
				quantityRequested=random.randint(1, 20),
				fault=random.choice(Fault.objects.all()),
				user=random.choice(User.objects.filter(role='engineer')),
				approved_by=random.choice(User.objects.filter(role__in=['supervisor', 'human-resource'])),
				approved=random.choice([True, False]),
				rejected=random.choice([True, False])
			)

		# Create 18 RequestComponents
		for _ in range(18):
			RequestComponent.objects.create(
				name=random.choice(component_names),
				quantityRequested=random.randint(1, 20),
				fault=random.choice(Fault.objects.all()),
				user=random.choice(User.objects.filter(role='engineer')),
				approved_by=random.choice(User.objects.filter(role__in=['supervisor', 'human-resource'])),
				approved=random.choice([True, False]),
				rejected=random.choice([True, False])
			)

		# Create 23 UnconfirmedParts
		for _ in range(23):
			UnconfirmedPart.objects.create(
				name=random.choice(part_names),
				quantity=random.randint(1, 20),
				user=random.choice(User.objects.filter(role='engineer')),
				status=random.choice([True, False]),
				approved_by=random.choice(User.objects.filter(role__in=['supervisor', 'human-resource']))
			)

		# assign random state and location to all users
		states = list(State.objects.all())
		locations = list(Location.objects.all())
		for user in User.objects.all():
			user.state = random.choice(states)
			user.location = random.choice(locations)
			user.save()

		# create account for myself as admin user
		User.objects.create_user(
			username='dafeman',
			email='ogagadafetite@gmail.com',
			password='debbydafe',
			is_superuser=True,
			is_staff=True
		)

		self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data'))
