// Define a class called "Person"
class Person {
  // Constructor to initialize the person's name and age
  constructor(public name: string, public age: number) {}

  // Method to greet the person
  greet() {
    console.log(`Hello, my name is ${this.name} and I am ${this.age} years old.`);
  }
}

// Create an instance of the Person class
const person1 = new Person("Alice", 30);

// Call the greet method
person1.greet();

// Define an array of persons
const people: Person[] = [
  person1,
  new Person("Bob", 25),
  new Person("Charlie", 35)
];

// Iterate through the array and greet each person
for (const person of people) {
  person.greet();
}

