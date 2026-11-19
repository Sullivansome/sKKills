import XCTest
@testable import Greeter

final class GreeterTests: XCTestCase {
    func testGreeting() {
        XCTAssertEqual(Greeter(name: "Ada").greeting(), "Hello, Ada!")
    }
}
