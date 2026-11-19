public struct Greeter {
    public let name: String

    public init(name: String) {
        self.name = name
    }

    public func greeting() -> String {
        "Hello, \(name)!"
    }

    public func farewell() -> String {
        "Goodbye, \(name)."
    }
}
