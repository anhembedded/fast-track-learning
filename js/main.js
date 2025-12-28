document.addEventListener('DOMContentLoaded', () => {

    const glossaryData = {
        'unit-testing': {
        short: "Một phương pháp kiểm thử phần mềm mà các đơn vị mã nguồn riêng lẻ (components, functions) được kiểm tra để xác định xem chúng có hoạt động đúng như mong đợi hay không.",
            long: "Unit Testing là cấp độ kiểm thử phần mềm cơ bản nhất, tập trung vào việc xác minh tính đúng đắn của các thành phần nhỏ nhất và có thể cô lập được trong một ứng dụng (gọi là 'unit'). Một unit có thể là một hàm, một phương thức, một lớp, hoặc một module. Mục tiêu của Unit Testing là đảm bảo mỗi đơn vị hoạt động chính xác theo thiết kế trước khi tích hợp chúng lại với nhau."
        },
        'unit-test': {
            short: "Một bài kiểm thử cụ thể cho một đơn vị mã nguồn nhỏ, cô lập.",
            long: "Là một đoạn mã được viết ra để thực thi một 'unit' và kiểm tra một khía cạnh cụ thể trong hành vi của nó. Một unit test tốt thường tuân theo mẫu AAA (Arrange-Act-Assert), chạy nhanh, và hoàn toàn độc lập với các test khác."
        },
        'regression': {
            short: "Một lỗi khiến một tính năng đã hoạt động bình thường bỗng dưng bị hỏng sau khi có sự thay đổi trong mã nguồn.",
            long: "Regression là một loại bug xuất hiện trở lại sau khi một phần của phần mềm được thay đổi. Bộ unit test đóng vai trò như một 'mạng lưới an toàn' để tự động phát hiện các lỗi regression này, cho phép lập trình viên tự tin hơn khi tái cấu trúc hoặc thêm tính năng mới."
        },
        'tight-coupling': {
            short: "Tình trạng các class/module phụ thuộc quá nhiều vào chi tiết cài đặt của nhau, khiến việc thay đổi một thành phần dễ làm hỏng các thành phần khác.",
            long: "Tight Coupling (liên kết chặt chẽ) xảy ra khi các thành phần trong hệ thống có sự phụ thuộc sâu sắc và chi tiết lẫn nhau. Điều này làm cho hệ thống trở nên khó thay đổi, khó bảo trì và khó viết unit test, vì không thể dễ dàng cô lập một thành phần để kiểm tra mà không cần đến các thành phần phụ thuộc của nó."
        },
        'refactor': {
            short: "Quá trình thay đổi cấu trúc mã nguồn bên trong mà không làm thay đổi hành vi có thể quan sát được bên ngoài.",
            long: "Refactoring là một kỹ thuật quan trọng trong phát triển phần mềm để cải thiện thiết kế, khả năng đọc và bảo trì của mã nguồn mà không làm thay đổi chức năng của nó. Một bộ unit test tốt là điều kiện tiên quyết để có thể refactor một cách an toàn."
        },
        'boilerplate': {
            short: "Các đoạn mã lặp đi lặp lại và ít mang lại giá trị logic, thường cần thiết cho các yêu cầu cú pháp hoặc cấu hình.",
            long: "Trong testing, boilerplate có thể là mã lặp đi lặp lại để thiết lập môi trường test (phần Arrange). Các mẫu như Test Data Builder giúp giảm thiểu boilerplate và làm cho ý định của bài test trở nên rõ ràng hơn."
        },
        'false-positive': {
            short: "Một kết quả test báo lỗi (fail) trong khi chức năng của ứng dụng thực sự vẫn đúng. Thường xảy ra do test quá mong manh.",
            long: "False Positive là một trong những vấn đề nghiêm trọng nhất của một bộ test. Khi nó xảy ra thường xuyên, lập trình viên sẽ mất niềm tin vào bộ test và có xu hướng bỏ qua các cảnh báo, dẫn đến nguy cơ bỏ lọt lỗi thật sự. Nguyên nhân chính thường là do test bị gắn vào chi tiết cài đặt."
        },
        'redundant': {
            short: "Thừa thãi, lặp lại. Một bài test thừa thãi là khi nó kiểm tra cùng một hành vi đã được một bài test khác kiểm tra rồi.",
            long: "Các bài test thừa thãi làm tăng chi phí bảo trì mà không tăng thêm giá trị bảo vệ. Mỗi hành vi quan trọng chỉ nên được kiểm tra bởi một bài test duy nhất."
        },
        'test-pyramid': {
            short: "Một mô hình chiến lược kiểm thử, khuyến khích viết nhiều unit test, ít integration test hơn và rất ít E2E test.",
            long: "Kim tự tháp Kiểm thử là một hướng dẫn trực quan về việc phân bổ nỗ lực kiểm thử. Nền tảng của kim tự tháp là Unit Test (nhiều, nhanh, rẻ), tầng giữa là Integration Test (ít hơn, chậm hơn), và đỉnh là E2E Test (rất ít, chậm, đắt đỏ). Mô hình này giúp tối ưu hóa hiệu quả và tốc độ của bộ test."
        },
        'integration-test': {
            short: "Kiểm thử sự tương tác giữa hai hoặc nhiều thành phần của hệ thống, hoặc với các hệ thống bên ngoài như database.",
            long: "Integration Test xác minh rằng các đơn vị riêng lẻ có thể làm việc cùng nhau một cách chính xác. Nó rất quan trọng để phát hiện các lỗi ở giao diện (interface) giữa các module hoặc giữa ứng dụng và các dịch vụ bên ngoài."
        },
        'e2e-test': {
            short: "Kiểm thử toàn bộ luồng ứng dụng từ đầu đến cuối, mô phỏng hành vi của người dùng thật.",
            long: "End-to-End (E2E) Test là cấp độ kiểm thử cao nhất, kiểm tra toàn bộ hệ thống trong một môi trường gần giống với production nhất. Nó cung cấp sự tự tin cao nhất nhưng cũng chậm và tốn kém nhất để viết và bảo trì."
        },
        'database': {
            short: "Một hệ thống có tổ chức để lưu trữ và truy xuất dữ liệu điện tử.",
            long: "Trong ngữ cảnh testing, database của ứng dụng thường được coi là một chi tiết cài đặt và không nên được mock trong unit test, mà nên được kiểm tra thông qua integration test."
        },
        'api': {
            short: "Giao diện lập trình ứng dụng (Application Programming Interface), một tập hợp các quy tắc cho phép các chương trình phần mềm khác nhau giao tiếp với nhau.",
            long: "API định nghĩa các phương thức và định dạng dữ liệu mà một ứng dụng có thể sử dụng để tương tác với một ứng dụng khác. Kiểm thử API là một phần quan trọng của integration testing."
        },
        'aaa': {
            short: "Mẫu cấu trúc Arrange-Act-Assert, một cách phổ biến để tổ chức các bài test cho dễ đọc và dễ bảo trì.",
            long: "Mẫu AAA chia một bài test thành ba phần rõ ràng: Arrange (chuẩn bị dữ liệu và môi trường), Act (thực thi hành vi cần kiểm tra), và Assert (xác minh kết quả). Cấu trúc này giúp tăng tính rõ ràng và nhất quán cho bộ test."
        },
        'mock': {
            short: "Một đối tượng giả dùng để giả lập và xác minh các tương tác đi ra (outcoming interactions) từ SUT đến các hệ thống bên ngoài.",
            long: "Mock là một loại Test Double tập trung vào việc kiểm tra hành vi. Nó ghi lại các lời gọi hàm mà SUT thực hiện lên nó, và trong phần Assert, ta sẽ kiểm tra xem các lời gọi đó có đúng như mong đợi không. Mock được dùng để test các Command."
        },
        'stub': {
            short: "Một đối tượng giả dùng để cung cấp dữ liệu đầu vào (input) được kiểm soát cho SUT, giúp mô phỏng các trạng thái khác nhau.",
            long: "Stub là một loại Test Double tập trung vào việc cung cấp trạng thái. Nó trả về các giá trị được định sẵn khi phương thức của nó được gọi, giúp SUT có dữ liệu để hoạt động. Không nên xác minh (verify) các lời gọi đến Stub."
        },
        'code-coverage': {
            short: "Một chỉ số đo lường tỷ lệ phần trăm mã nguồn được thực thi bởi bộ test. Dùng để tìm ra những phần chưa được test.",
            long: "Code Coverage là một công cụ hữu ích để xác định các phần của mã nguồn chưa được kiểm thử. Tuy nhiên, nó không phải là thước đo chất lượng. Một bộ test có coverage 100% vẫn có thể là một bộ test tồi nếu nó thiếu các xác minh (assertion) quan trọng."
        },
        'london-school': {
            short: "Một trường phái unit testing (còn gọi là Mockist) coi một class là một đơn vị và mock tất cả các dependency của nó.",
            long: "Trường phái London tập trung vào việc cách ly từng class và kiểm tra sự tương tác giữa chúng. Cách tiếp cận này có thể dẫn đến các bài test mong manh (brittle) vì chúng bị gắn chặt vào chi tiết cài đặt."
        },
        'classical-school': {
            short: "Một trường phái unit testing coi một hành vi nghiệp vụ là một đơn vị và chỉ mock các dependency bên ngoài, chậm.",
            long: "Trường phái Classical (Detroit) tập trung vào việc kiểm tra kết quả cuối cùng của một hành vi, cho phép một nhóm các class làm việc cùng nhau. Cách tiếp cận này tạo ra các bài test bền vững và có khả năng chống chịu refactoring cao hơn."
        },
        'test-double': {
            short: "Thuật ngữ chung cho bất kỳ đối tượng nào thay thế một đối tượng thật cho mục đích kiểm thử (bao gồm Mocks, Stubs, Fakes...).",
            long: "Test Doubles là một họ các đối tượng giả được sử dụng trong unit testing. Các loại chính bao gồm Dummy, Fake, Stub, Spy, và Mock. Mỗi loại phục vụ một mục đích khác nhau trong việc cách ly SUT."
        },
        'dependency': {
            short: "Một đối tượng hoặc module mà một đối tượng khác cần để thực hiện công việc của nó.",
            long: "Dependency (sự phụ thuộc) là một khía cạnh cơ bản trong thiết kế phần mềm. Quản lý dependency là một thách thức lớn, và các kỹ thuật như Dependency Injection giúp làm cho code trở nên dễ kiểm thử hơn."
        },
        'sut': {
            short: "System Under Test - Hệ thống đang được kiểm thử. Đây là đối tượng hoặc đơn vị mã nguồn mà bài test đang nhắm đến.",
            long: "SUT là thuật ngữ chuẩn để chỉ phần mã nguồn cụ thể mà một bài unit test đang kiểm tra. Việc xác định rõ SUT giúp giữ cho bài test tập trung và không lan sang kiểm tra các thành phần khác."
        },
        'implementation-details': {
            short: "Các bước xử lý, thuật toán, hoặc cấu trúc dữ liệu nội bộ được sử dụng để tạo ra một hành vi. Đây là 'cách làm' (how).",
            long: "Chi tiết cài đặt là những thứ xảy ra bên trong một class hoặc module. Việc viết test gắn chặt vào các chi tiết này là nguyên nhân chính gây ra các bài test mong manh (brittle test) vì chúng sẽ bị hỏng khi refactor."
        },
        'shared-dependency': {
            short: "Một dependency được chia sẻ giữa nhiều bài test, ví dụ như database hoặc file system, có thể gây ra sự phụ thuộc và xung đột nếu không được quản lý cẩn thận.",
            long: "Shared Dependency là một dependency mà các bài test không thể có một bản sao riêng cho mình (ví dụ: một database tĩnh). Việc tương tác với shared dependency làm cho các bài test trở thành integration test, và chúng cần được xử lý cẩn thận để đảm bảo tính độc lập giữa các test case."
        },
        'observable-behavior': {
            short: "Là kết quả hoặc trạng thái có thể quan sát được từ bên ngoài mà code mang lại để phục vụ mục tiêu của client. Đây là 'cái gì' (what).",
            long: "Hành vi quan sát được là những gì mà client của code quan tâm. Một bài test tốt chỉ nên kiểm tra vào hành vi này, và bỏ qua các chi tiết cài đặt. Điều này làm cho bài test trở nên bền vững và có khả năng chống chịu refactoring."
        },
        'public-api': {
            short: "Tập hợp các phương thức và thuộc tính của một class mà code bên ngoài (client) được phép truy cập và sử dụng.",
            long: "Public API tạo thành một 'hợp đồng' giữa class và các client của nó. Client chỉ nên tương tác với class thông qua Public API này. Một API được thiết kế tốt sẽ chỉ bao gồm các hành vi quan sát được."
        },
        'private-api': {
            short: "Tập hợp các phương thức và thuộc tính của một class chỉ được sử dụng trong nội bộ và không dành cho bên ngoài truy cập.",
            long: "Private API chứa các chi tiết cài đặt. Việc che giấu chúng khỏi client là một phần của nguyên tắc đóng gói (encapsulation) và giúp giảm sự phụ thuộc không cần thiết."
        },
        'encapsulation': {
            short: "Nguyên tắc che giấu thông tin, trong đó dữ liệu và các phương thức xử lý dữ liệu đó được đóng gói lại với nhau, và chi tiết cài đặt được ẩn đi khỏi bên ngoài.",
            long: "Encapsulation (tính đóng gói) là một trong những trụ cột của lập trình hướng đối tượng. Nó giúp quản lý sự phức tạp bằng cách tạo ra các 'hộp đen' mà người dùng có thể sử dụng mà không cần biết nó hoạt động bên trong như thế nào."
        },
        'hexagonal-architecture': {
            short: "Một mẫu kiến trúc phần mềm nhằm tạo ra các ứng dụng có thể kết nối lỏng lẻo, tách biệt lõi logic khỏi các dịch vụ bên ngoài.",
            long: "Kiến trúc Lục giác (còn gọi là Ports and Adapters) giúp tách biệt lõi logic nghiệp vụ của ứng dụng khỏi các mối quan tâm về kỹ thuật như UI, database, hay các API bên ngoài. Điều này làm cho ứng dụng dễ kiểm thử, dễ bảo trì và dễ dàng thay đổi công nghệ."
        },
        'domain-layer': {
             short: "Lớp trung tâm trong kiến trúc phần mềm, chứa đựng logic và quy tắc nghiệp vụ cốt lõi của ứng dụng.",
             long: "Domain Layer là trái tim của ứng dụng, nơi các quy tắc và quy trình kinh doanh được định nghĩa. Lớp này không nên có bất kỳ sự phụ thuộc nào vào các lớp bên ngoài như lớp trình bày hay lớp truy cập dữ liệu."
        },
        'application-services-layer': {
            short: "Lớp bao bọc Domain Layer, điều phối các yêu cầu từ bên ngoài, gọi logic nghiệp vụ và trả về kết quả.",
            long: "Application Services Layer hoạt động như một facade cho lõi nghiệp vụ. Nó nhận các yêu cầu, sử dụng các đối tượng trong Domain Layer để thực hiện công việc, và điều phối các tác vụ như lưu trữ dữ liệu hoặc gửi thông báo."
        }
    };

    // --- Theme Toggler ---
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    const setTheme = (theme) => {
        htmlElement.classList.remove('light', 'dark');
        htmlElement.classList.add(theme);
        localStorage.setItem('theme', theme);
    };

    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);

    themeToggle.addEventListener('click', () => {
        const currentTheme = htmlElement.classList.contains('dark') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });

    // --- SPA Navigation ---
    const navItems = document.querySelectorAll('.nav-item');
    const contentSections = document.querySelectorAll('.content-section');

    const navigateTo = (targetId) => {
        navItems.forEach(item => {
            item.classList.toggle('active', item.dataset.target === targetId);
        });
        contentSections.forEach(section => {
            section.classList.toggle('active', section.id === targetId);
        });
        document.querySelector('.main-content').scrollTop = 0;
    };

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetId = item.dataset.target;
            navigateTo(targetId);
        });
    });

    // --- Keyword Tooltip Initialization ---
    const keywords = document.querySelectorAll('.keyword');
    keywords.forEach(keyword => {
        const keywordId = keyword.dataset.keyword;
        const definition = glossaryData[keywordId]?.short;

        if (definition) {
            const tooltip = document.createElement('span');
            tooltip.className = 'tooltip';
            tooltip.textContent = definition;
            keyword.appendChild(tooltip);
        }
    });

    // --- Glossary Page Generation ---
    const generateGlossary = () => {
        const glossarySection = document.getElementById('glossary');
        const glossaryContent = glossarySection.querySelector('p').nextElementSibling; // Get element after the intro 'p'

        let html = '';
        const sortedKeys = Object.keys(glossaryData).sort();

        sortedKeys.forEach(key => {
            const term = glossaryData[key];
            const termName = key.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            html += `<h3>${termName}</h3>`;
            html += `<p>${term.long}</p>`;
        });

        // If there's no dedicated container, append after the intro paragraph
        if(glossaryContent){
            glossaryContent.innerHTML = html;
        } else {
            glossarySection.innerHTML += html;
        }
    };

    // --- Initial Load ---
    generateGlossary();
    navigateTo('home');
    feather.replace();
});
